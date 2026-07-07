import json

from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.report_builder import generate_reports
from agentguard.assessment.risk_engine import assess_workflow


def test_json_markdown_and_html_reports_are_generated(tmp_path):
    workflow = load_demo_workflow("financial_advisor_copilot")
    result = assess_workflow(workflow)

    paths = generate_reports(workflow, result, tmp_path)

    assert paths["json"].exists()
    assert paths["markdown"].exists()
    assert paths["html"].exists()
    markdown_text = paths["markdown"].read_text(encoding="utf-8")
    html_text = paths["html"].read_text(encoding="utf-8")
    assert "AgentGuard AI Assessment" in markdown_text
    assert "Disclaimer" in markdown_text
    assert "Risk Scoring Explanation" in markdown_text
    assert "<html" in html_text.lower()
    assert "Portfolio prototype only" in html_text

    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert payload["workflow_id"] == "financial_advisor_copilot"
    assert payload["overall_risk_level"] == result.overall_risk_level
