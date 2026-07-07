import os
import subprocess
import sys

from agentguard.config import project_root


def test_cli_assess_command_exits_successfully():
    root = project_root()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "agentguard.main",
            "assess",
            "--case",
            "financial_advisor_copilot",
        ],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "overall_risk_level:" in completed.stdout
    assert "reports/json/financial_advisor_copilot_assessment.json" in completed.stdout
