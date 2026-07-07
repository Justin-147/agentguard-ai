"""Run the AgentGuard AI local demo checks."""

from __future__ import annotations

import subprocess
import sys

COMMANDS = [
    [sys.executable, "-m", "ruff", "check", "."],
    [sys.executable, "-m", "compileall", "src", "tests", "scripts"],
    [sys.executable, "-m", "mypy", "src/agentguard"],
    [sys.executable, "-m", "pytest"],
    [sys.executable, "-m", "agentguard.main", "validate"],
    [
        sys.executable,
        "-m",
        "agentguard.main",
        "validate-workflow",
        "--input",
        "examples/workflows/high_risk_autonomous_agent.json",
    ],
    [sys.executable, "-m", "agentguard.main", "list-cases"],
    [
        sys.executable,
        "-m",
        "agentguard.main",
        "assess",
        "--case",
        "financial_advisor_copilot",
        "--as-of",
        "2026-07-06",
        "--output-root",
        ".tmp/demo",
    ],
    [
        sys.executable,
        "-m",
        "agentguard.main",
        "assess-all",
        "--as-of",
        "2026-07-06",
        "--output-root",
        ".tmp/demo",
    ],
    [sys.executable, "-m", "build"],
]


def main() -> int:
    for command in COMMANDS:
        print("+ " + " ".join(command))
        subprocess.run(command, check=True)
    print("demo_status=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
