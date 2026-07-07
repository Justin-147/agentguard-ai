import json
import os
import subprocess
import sys
from pathlib import Path

from agentguard.config import load_demo_cases, project_root


def _run_cli(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    root = cwd or project_root()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")
    return subprocess.run(
        [sys.executable, "-m", "agentguard.main", *args],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_assess_uses_tmp_output_root_and_as_of(tmp_path):
    completed = _run_cli(
        [
            "assess",
            "--case",
            "financial_advisor_copilot",
            "--as-of",
            "2026-07-06T09:00:00+08:00",
            "--output-root",
            str(tmp_path),
        ]
    )

    assert completed.returncode == 0, completed.stderr
    output_file = tmp_path / "reports" / "json" / "financial_advisor_copilot_assessment.json"
    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["generated_at"] == "2026-07-06T01:00:00"


def test_cli_assess_all_generates_all_demo_cases(tmp_path):
    completed = _run_cli(["assess-all", "--output-root", str(tmp_path), "--as-of", "2026-07-06"])

    assert completed.returncode == 0, completed.stderr
    for case_name in load_demo_cases():
        assert (tmp_path / "reports" / "json" / f"{case_name}_assessment.json").exists()


def test_cli_list_validate_and_export_schema(tmp_path):
    list_result = _run_cli(["list-cases"])
    validate_result = _run_cli(["validate"])
    schema_path = tmp_path / "workflow_schema.json"
    schema_result = _run_cli(["export-schema", "--output", str(schema_path)])

    assert list_result.returncode == 0
    assert "financial_advisor_copilot" in list_result.stdout
    assert "Financial Advisor Copilot" in list_result.stdout
    assert validate_result.returncode == 0
    assert "status: passed" in validate_result.stdout
    assert schema_result.returncode == 0
    assert json.loads(schema_path.read_text(encoding="utf-8"))["title"] == "AgentWorkflow"
