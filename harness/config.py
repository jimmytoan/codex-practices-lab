"""Paths, prices and the condition matrix."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "target"  # the clean repo every run starts from
HIDDEN = ROOT / "hidden"  # hidden tests; never copied into a working copy
RESULTS = ROOT / "results"
CONDITIONS = ROOT / "conditions"  # generated AGENTS.md variants (inspectable, committed)
LAB_CODEX_HOME = ROOT / ".codex-home"  # holds auth.json from `codex login --with-api-key`; git-ignored

# Working copies and per-run CODEX_HOMEs live outside the lab repo, so the hidden tests are not in any parent
# directory of a working copy.
RUNTIME = Path(os.environ.get("LAB_RUNTIME", Path.home() / ".cache" / "codex-practices-lab"))
WORK = RUNTIME / "work"
VENV_BIN = RUNTIME / "venv" / "bin"  # python + pytest, first on the agent's PATH
PYTHON = VENV_BIN / "python"

CODEX = shutil.which("codex") or "codex"

# List prices per million tokens (OpenAI pricing page, standard tier, short context, read 17 November 2026).
# "write_30m" and "write_12h" are the two cache-write prices; Codex reports cache_write_input_tokens without
# saying which applies, so cost_usd uses the 12h price (upper bound) and cost_usd_low the 30m price.
PRICES = {
    "gpt-6.1-sol": {"input": 2.00, "cached": 0.10, "write_30m": 2.50, "write_12h": 5.00, "output": 10.00},
    "gpt-6.1-terra": {"input": 1.00, "cached": 0.05, "write_30m": 1.25, "write_12h": 2.50, "output": 5.00},
    "gpt-6-luna": {"input": 0.10, "cached": 0.01, "write_30m": 0.125, "write_12h": 0.25, "output": 0.50},
    "gpt-5.6-sol": {"input": 4.00, "cached": 0.40, "write_30m": 5.00, "write_12h": 10.00, "output": 20.00},
}


def cost(model: str, usage: dict, write_price: str = "write_12h") -> float:
    """Dollar cost of one usage block. input_tokens includes cached and cache-write tokens;
    output_tokens includes reasoning tokens."""
    p = PRICES[model]
    inp = usage.get("input_tokens", 0)
    cached = usage.get("cached_input_tokens", 0)
    write = usage.get("cache_write_input_tokens", 0)
    plain = max(inp - cached - write, 0)
    out = usage.get("output_tokens", 0)
    return (plain * p["input"] + cached * p["cached"] + write * p[write_price] + out * p["output"]) / 1e6


@dataclass(frozen=True)
class Condition:
    name: str
    agents: str = "short"  # none | short | bloated | rule_early | rule_late
    prompt: str = "four_part"  # four_part | one_line
    mode: str = "direct"  # direct | plan | review_same | review_fresh
    effort: str = "medium"
    variant: str = ""  # review only: buggy | clean
    tasks: str = "all"  # all | rule | seeded


# Every test changes one thing from BASE. BASE is shared by tests 1, 3, 4 and 5.
CONDITION_LIST = [
    Condition("base"),
    Condition("agents_none", agents="none"),
    Condition("agents_bloated", agents="bloated"),
    Condition("rule_early", agents="rule_early", tasks="rule"),
    Condition("rule_late", agents="rule_late", tasks="rule"),
    Condition("prompt_oneline", prompt="one_line"),
    Condition("plan", mode="plan"),
    Condition("effort_low", effort="low"),
    Condition("effort_high", effort="high"),
    Condition("review_same_buggy", mode="review_same", variant="buggy", tasks="seeded"),
    Condition("review_fresh_buggy", mode="review_fresh", variant="buggy", tasks="seeded"),
    Condition("review_same_clean", mode="review_same", variant="clean", tasks="seeded"),
    Condition("review_fresh_clean", mode="review_fresh", variant="clean", tasks="seeded"),
]
CONDITIONS_BY_NAME = {c.name: c for c in CONDITION_LIST}

# Which conditions make up each of the six tests (for the report).
TESTS = {
    "1 AGENTS.md size": ["agents_none", "base", "agents_bloated"],
    "2 32 KiB limit": ["agents_none", "base", "rule_early", "rule_late"],
    "3 prompt shape": ["prompt_oneline", "base"],
    "4 plan first": ["base", "plan"],
    "5 reasoning effort": ["effort_low", "base", "effort_high"],
    "6 review session": ["review_same_buggy", "review_fresh_buggy", "review_same_clean", "review_fresh_clean"],
}
