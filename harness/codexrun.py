"""Drive `codex exec --json` and parse what it reports.

Verified against codex-cli 0.169.0 (see PLAN.md, "What the probe showed"):
- `-m MODEL` and `-c model_reasoning_effort="low"` take effect (the rollout's turn_context shows both).
- The JSON stream emits thread.started, turn.started, item.started/item.completed, turn.completed (with `usage`),
  turn.failed and error.
- `usage` in turn.completed is the total for that invocation: input_tokens (includes cached_input_tokens and
  cache_write_input_tokens), output_tokens (includes reasoning_output_tokens).
- `codex exec resume <thread_id>` continues a session; `-s` is not accepted there, so the sandbox is set with
  `-c sandbox_mode=...`.
- The rollout file CODEX_HOME/sessions/YYYY/MM/DD/rollout-*-<thread_id>.jsonl gets a token_usage_record after every
  model response, which is what the live spend guard reads.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from .config import CODEX, LAB_CODEX_HOME, VENV_BIN, cost


@dataclass
class Invocation:
    events: list[dict] = field(default_factory=list)
    thread_id: str | None = None
    usage: dict = field(default_factory=dict)
    status: str = "ok"  # ok | error | timeout | cost_cap
    error: str | None = None
    exit_code: int | None = None
    wall_s: float = 0.0
    final_message: str = ""
    commands: list[str] = field(default_factory=list)
    stderr_tail: str = ""


def fresh_codex_home(dest: Path) -> Path:
    """A per-run CODEX_HOME holding only the API-key auth and a minimal config, so no state (sessions,
    memories, caches) carries over between runs and ~/.codex is never read."""
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy(LAB_CODEX_HOME / "auth.json", dest / "auth.json")
    (dest / "config.toml").write_text('cli_auth_credentials_store = "file"\n')
    return dest


def agent_env(codex_home: Path) -> dict:
    """Environment for codex and the commands it runs: no API keys, lab python first on PATH."""
    node_bin = str(Path(CODEX).parent)
    return {
        "PATH": f"{VENV_BIN}:{node_bin}:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin",
        "HOME": os.environ["HOME"],
        "CODEX_HOME": str(codex_home),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
        "LANG": "en_US.UTF-8",
        "USER": os.environ.get("USER", "lab"),
        "SHELL": "/bin/zsh",
    }


def parse_events(lines: list[str]) -> Invocation:
    inv = Invocation()
    for line in lines:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        inv.events.append(ev)
        t = ev.get("type")
        if t == "thread.started":
            inv.thread_id = ev.get("thread_id")
        elif t == "turn.completed":
            inv.usage = ev.get("usage", {})
        elif t in ("turn.failed", "error"):
            inv.status = "error"
            inv.error = json.dumps(ev)[:800]
        elif t == "item.completed":
            item = ev.get("item", {})
            if item.get("type") == "command_execution":
                inv.commands.append(item.get("command", ""))
            elif item.get("type") == "agent_message":
                inv.final_message = item.get("text", "")
    if inv.status == "ok" and not inv.usage:
        inv.status = "error"
        inv.error = inv.error or "no turn.completed event"
    return inv


def find_rollout(codex_home: Path, thread_id: str) -> Path | None:
    hits = sorted((codex_home / "sessions").glob(f"*/*/*/rollout-*{thread_id}.jsonl"))
    return hits[-1] if hits else None


def rollout_spend(path: Path, start_line: int, model: str) -> float:
    """Upper-bound spend of the token_usage_records written after line `start_line`."""
    total = 0.0
    try:
        with path.open() as fh:
            for i, line in enumerate(fh):
                if i < start_line or '"token_usage_record"' not in line:
                    continue
                try:
                    total += cost(model, json.loads(line)["payload"]["usage"])
                except (json.JSONDecodeError, KeyError):
                    pass
    except FileNotFoundError:
        pass
    return total


def count_lines(path: Path | None) -> int:
    if not path or not path.exists():
        return 0
    with path.open() as fh:
        return sum(1 for _ in fh)


def run(prompt: str, *, cwd: Path, codex_home: Path, model: str, effort: str, sandbox: str,
        resume_thread: str | None = None, output_schema: Path | None = None, events_out: Path | None = None,
        timeout_s: int = 900, spend_cap_usd: float = 1.0) -> Invocation:
    """One `codex exec` (or `codex exec resume`) invocation, killed if it runs past timeout_s or its own
    upper-bound spend passes spend_cap_usd."""
    common = ["--json", "-m", model, "-c", f'model_reasoning_effort="{effort}"', "-c", "allow_login_shell=false"]
    if output_schema:
        common += ["--output-schema", str(output_schema)]
    if resume_thread:
        cmd = [CODEX, "exec", "resume", resume_thread, *common, "-c", f'sandbox_mode="{sandbox}"', prompt]
    else:
        cmd = [CODEX, "exec", *common, "-s", sandbox, "-C", str(cwd), prompt]

    rollout = find_rollout(codex_home, resume_thread) if resume_thread else None
    start_line = count_lines(rollout)
    t0 = time.time()
    proc = subprocess.Popen(cmd, cwd=cwd, env=agent_env(codex_home), stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    lines: list[str] = []
    stderr: list[str] = []
    t_out = threading.Thread(target=lambda: lines.extend(proc.stdout), daemon=True)
    t_err = threading.Thread(target=lambda: stderr.extend(proc.stderr), daemon=True)
    t_out.start()
    t_err.start()

    killed = None
    thread_id = resume_thread
    while proc.poll() is None:
        time.sleep(2)
        if thread_id is None:
            for line in list(lines[:3]):
                if '"thread.started"' in line:
                    thread_id = json.loads(line).get("thread_id")
        if thread_id and rollout is None:
            rollout = find_rollout(codex_home, thread_id)
        if rollout and rollout_spend(rollout, start_line, model) > spend_cap_usd:
            killed = "cost_cap"
        elif time.time() - t0 > timeout_s:
            killed = "timeout"
        if killed:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
            break
    proc.wait()
    t_out.join(5)
    t_err.join(5)

    inv = parse_events(lines)
    inv.exit_code = proc.returncode
    inv.wall_s = round(time.time() - t0, 1)
    inv.stderr_tail = "".join(stderr)[-1500:]
    inv.thread_id = inv.thread_id or thread_id
    if killed:
        inv.status = killed
        inv.error = killed
        # no turn.completed: take the usage the rollout recorded before the kill
        if rollout:
            inv.usage = rollout_usage(rollout, start_line)
    elif inv.status == "ok" and proc.returncode != 0:
        inv.status = "error"
        inv.error = f"exit {proc.returncode}: {inv.stderr_tail[-400:]}"
    if events_out:
        events_out.write_text("".join(lines))
    return inv


def rollout_usage(path: Path, start_line: int) -> dict:
    keys = ["input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens"]
    total = dict.fromkeys(keys, 0)
    with path.open() as fh:
        for i, line in enumerate(fh):
            if i >= start_line and '"token_usage_record"' in line:
                usage = json.loads(line)["payload"]["usage"]
                for k in keys:
                    total[k] += usage.get(k, 0)
    return total


def rollout_facts(path: Path | None) -> dict:
    """What Codex actually loaded and applied, from its own rollout: the AGENTS.md text it put in context,
    and the model and effort of each turn."""
    facts = {"agents_loaded_bytes": None, "agents_loaded_text_tail": None, "turns": []}
    if not path or not path.exists():
        return facts
    with path.open() as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") == "world_state" and facts["agents_loaded_bytes"] is None:
                agents = (d.get("payload", {}).get("state") or {}).get("agents_md")
                if agents:
                    text = agents.get("text") or ""
                    facts["agents_loaded_bytes"] = len(text.encode())
                    facts["agents_loaded_text_tail"] = text[-200:]
                    facts["agents_loaded_has_rule"] = "shoplib.errors.ShopError" in text
                else:
                    facts["agents_loaded_bytes"] = 0
                    facts["agents_loaded_has_rule"] = False
            elif d.get("type") == "turn_context":
                p = d.get("payload", {})
                facts["turns"].append({"model": p.get("model"), "effort": p.get("effort"),
                                       "sandbox": (p.get("sandbox_policy") or {}).get("type")})
    return facts
