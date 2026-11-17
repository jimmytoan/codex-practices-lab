"""Working copies, edits, diffs, scope checks and hidden-test grading. No model calls here."""

from __future__ import annotations

import fnmatch
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from . import agentsmd
from .config import HIDDEN, PYTHON, TARGET
from .tasks import Edit

GIT_ENV = {"GIT_AUTHOR_NAME": "lab", "GIT_AUTHOR_EMAIL": "lab@example.invalid",
           "GIT_COMMITTER_NAME": "lab", "GIT_COMMITTER_EMAIL": "lab@example.invalid"}


def git(repo: Path, *args: str, check: bool = True) -> str:
    env = {**os.environ, **GIT_ENV}
    out = subprocess.run(["git", *args], cwd=repo, env=env, capture_output=True, text=True)
    if check and out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def make_copy(dest: Path, agents_kind: str) -> str:
    """Fresh copy of the target repo with the given AGENTS.md, committed. Returns the base commit."""
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(TARGET, dest, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".git"))
    text = agentsmd.build(agents_kind)
    if text is not None:
        (dest / "AGENTS.md").write_text(text)
    git(dest, "init", "-q", "-b", "main")
    git(dest, "add", "-A")
    git(dest, "commit", "-q", "-m", "base")
    return git(dest, "rev-parse", "HEAD").strip()


def apply_edits(repo: Path, edits: list[Edit]) -> None:
    for path, old, new in edits:
        f = repo / path
        text = f.read_text()
        if text.count(old) != 1:
            raise ValueError(f"edit for {path} matches {text.count(old)} times: {old[:60]!r}")
        f.write_text(text.replace(old, new))


def changed_files(repo: Path, base: str) -> list[str]:
    """Every path that differs from the base commit, committed or not (git-ignored files excluded)."""
    git(repo, "add", "-A")
    out = git(repo, "diff", "--cached", "--name-only", "--no-renames", base)
    return sorted(p for p in out.splitlines() if p)


def diff(repo: Path, base: str) -> str:
    git(repo, "add", "-A")
    return git(repo, "diff", "--cached", "--no-renames", base)


def out_of_scope(paths: list[str], scope: list[str]) -> list[str]:
    return [p for p in paths if not any(fnmatch.fnmatch(p, pat) for pat in scope)]


def run_pytest(test_file: Path, src: Path, cwd: Path | None = None, timeout: int = 180) -> dict:
    """Run one test file against `src` and return {"passed": [...], "failed": [...], "error": str|None}."""
    with tempfile.TemporaryDirectory(prefix="grade-") as tmp:
        tmp = Path(tmp)
        test_copy = tmp / test_file.name
        shutil.copy(test_file, test_copy)
        xml = tmp / "junit.xml"
        env = {"PATH": f"{PYTHON.parent}:/usr/bin:/bin", "PYTHONPATH": str(src), "PYTHONDONTWRITEBYTECODE": "1",
               "HOME": str(tmp)}
        try:
            proc = subprocess.run([str(PYTHON), "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={xml}",
                                   "--rootdir", str(tmp), str(test_copy)],
                                  cwd=cwd or tmp, env=env, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"passed": [], "failed": [], "error": "timeout"}
        if not xml.exists():
            return {"passed": [], "failed": [], "error": (proc.stdout + proc.stderr)[-1500:]}
        passed, failed = [], []
        for case in ET.parse(xml).getroot().iter("testcase"):
            name = case.get("name")
            bad = any(child.tag in ("failure", "error") for child in case)
            (failed if bad else passed).append(name)
        error = None if (passed or failed) else (proc.stdout + proc.stderr)[-1500:]
        return {"passed": sorted(passed), "failed": sorted(failed), "error": error}


def grade_hidden(repo: Path, task_id: str) -> dict:
    r = run_pytest(HIDDEN / "tasks" / task_id / "test_task.py", repo / "src")
    r["ok"] = bool(r["passed"]) and not r["failed"] and not r["error"]
    return r


def grade_rule(repo: Path, task_id: str) -> dict | None:
    f = HIDDEN / "rules" / f"test_{task_id}.py"
    if not f.exists():
        return None
    r = run_pytest(f, repo / "src")
    r["ok"] = bool(r["passed"]) and not r["failed"] and not r["error"]
    return r


def grade_visible(repo: Path, timeout: int = 180) -> dict:
    """The repo's own test suite, including any tests the agent added."""
    env = {"PATH": f"{PYTHON.parent}:/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1", "HOME": str(repo)}
    try:
        proc = subprocess.run([str(PYTHON), "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=repo, env=env,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "tail": "timeout"}
    return {"ok": proc.returncode == 0, "tail": proc.stdout.strip().splitlines()[-1:] if proc.stdout.strip() else proc.stderr[-300:]}
