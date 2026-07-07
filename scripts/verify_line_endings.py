"""Verify line-ending consistency for release-critical files."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "pyproject.toml",
    ".gitattributes",
    ".github/workflows/tests.yml",
    "src/agentguard/main.py",
    "src/agentguard/models.py",
    "src/agentguard/assessment/risk_engine.py",
    "src/agentguard/assessment/report_builder.py",
    "src/agentguard/writers/formatting.py",
    "src/agentguard/dashboard/app.py",
    "tests/test_cli.py",
    "tests/test_report_generation.py",
    "tests/test_dashboard_helpers.py",
    "scripts/run_demo.py",
]
MIN_LF_COUNT = 1
MAX_LITERAL_NEWLINES = 20


def has_cr_only_line_ending(data: bytes) -> bool:
    for index, byte in enumerate(data):
        if byte == 13 and (index + 1 == len(data) or data[index + 1] != 10):
            return True
    return False


def main() -> int:
    failures: list[str] = []
    for relative_path in CHECKED_FILES:
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"{relative_path}: missing")
            continue
        data = path.read_bytes()
        lf_count = data.count(b"\n")
        literal_newlines = data.count(br"\n")
        if has_cr_only_line_ending(data):
            failures.append(f"{relative_path}: contains CR-only line endings")
        if literal_newlines > MAX_LITERAL_NEWLINES:
            failures.append(
                f"{relative_path}: suspicious literal \\n count ({literal_newlines})"
            )
        if lf_count < MIN_LF_COUNT:
            failures.append(f"{relative_path}: too few LF line endings ({lf_count})")

    if failures:
        print("line_ending_status=failed")
        for failure in failures:
            print(f"failure: {failure}")
        return 1
    print("line_ending_status=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
