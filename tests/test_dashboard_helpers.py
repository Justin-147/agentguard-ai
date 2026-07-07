from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.dashboard.helpers import (
    comparison_dataframe,
    filter_findings,
    findings_to_dataframe,
)


def test_dashboard_helpers_handle_empty_findings():
    assert filter_findings([], severities=["high"]) == []
    assert findings_to_dataframe([]).empty


def test_filter_findings_by_score_and_risk_tag():
    result = assess_workflow(load_demo_workflow("high_risk_autonomous_agent"))
    filtered = filter_findings(
        result.findings,
        risk_tags=["external_action_risk"],
        min_score=0.5,
    )

    assert filtered
    assert all(finding.risk_tag == "external_action_risk" for finding in filtered)
    assert all(finding.risk_score >= 0.5 for finding in filtered)


def test_comparison_dataframe_has_expected_columns():
    workflows = [
        load_demo_workflow("financial_advisor_copilot"),
        load_demo_workflow("high_risk_autonomous_agent"),
    ]
    frame = comparison_dataframe(workflows)

    expected_columns = {
        "case",
        "name",
        "overall_score",
        "overall_risk_level",
        "findings_count",
    }
    assert expected_columns.issubset(frame.columns)
    assert len(frame) == 2
