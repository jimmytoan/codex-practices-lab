# Codex best-practices lab

Which pieces of OpenAI's official Codex advice change the numbers? Six tests, each changing one thing from a
baseline, run with `codex exec --json` against a small purpose-built repo whose tasks are graded by hidden tests.
No model grades anything.

| # | Advice | Conditions (`harness/config.py`) |
|---|---|---|
| 1 | Write an AGENTS.md, keep it short | `agents_none`, `base` (short file), `agents_bloated` (short + ~25 KiB filler) |
| 2 | AGENTS.md loading stops at 32 KiB | `rule_early`, `rule_late`: a test-checked rule before / after byte 32768 of a 40 KiB file |
| 3 | Prompt with goal, context, constraints, done-when | `prompt_oneline`, `base` (four-part) |
| 4 | Plan first | `base`, `plan` (read-only planning turn, then `codex exec resume` to implement) |
| 5 | Match reasoning effort to the task | `effort_low`, `base` (medium), `effort_high` |
| 6 | Review in a fresh session | `review_same_*` vs `review_fresh_*`, on seeded-bug and bug-free patches |

Baseline (`base`): short AGENTS.md, four-part prompt, no plan step, medium effort, `gpt-6.1-terra`.

## Layout
- `target/`: the repo every run starts from (`shoplib`, 10 tasks, visible tests).
- `hidden/`: hidden tests per task (`tasks/`) and rule checks (`rules/`). Never copied into a working copy.
- `harness/tasks.py`: prompts, scope, reference solutions and seeded bugs.
- `harness/agentsmd.py`: AGENTS.md variants (written to `conditions/`).
- `harness/codexrun.py`: drives `codex exec`, parses events, live per-run spend guard.
- `harness/run.py`: matrix, `--resume`, hard `--cap`. `harness/report.py`: tables. `harness/selftest.py`: no-model checks.
- `results/runs.jsonl`: one record per run; `results/raw/<run_id>/`: events, Codex rollout, diff, record.

## Running
```bash
npm install -g @openai/codex@0.169.0
CODEX_HOME=$PWD/.codex-home codex login --with-api-key < <(grep OPENAI_API_KEY .env | cut -d= -f2-)
uv venv ~/.cache/codex-practices-lab/venv && uv pip install --python ~/.cache/codex-practices-lab/venv/bin/python pytest
PY=~/.cache/codex-practices-lab/venv/bin/python
$PY -m harness.selftest
$PY -m harness.run --tag pilot --cap 5 --plan results/pilot-cells.json
$PY -m harness.report --tag pilot --out results/report-pilot.md
```

Isolation: every run gets its own `CODEX_HOME` (only the API-key `auth.json` and a two-line config), so the
user's `~/.codex` (settings, global AGENTS.md, memories) is never read. Working copies live under
`~/.cache/codex-practices-lab/work/`, outside this repo, so the hidden tests are not in any parent directory.
