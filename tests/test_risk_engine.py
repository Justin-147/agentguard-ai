from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.risk_engine import assess_workflow, generate_risk_findings


def _risk_tags(case_name: str) -> set[str]:
    workflow = load_demo_workflow(case_name)
    return {finding.risk_tag for finding in generate_risk_findings(workflow)}


def test_high_risk_autonomous_agent_is_high_or_critical():
    result = assess_workflow(load_demo_workflow("high_risk_autonomous_agent"))

    assert result.overall_risk_level in {"High", "Critical"}
    assert result.overall_score >= 0.55


def test_market_intelligence_agent_is_low_or_medium():
    result = assess_workflow(load_demo_workflow("market_intelligence_agent"))

    assert result.overall_risk_level in {"Low", "Medium"}


def test_external_email_without_approval_triggers_external_action_risk():
    assert "external_action_risk" in _risk_tags("customer_support_email_agent")


def test_sensitive_data_without_retention_triggers_data_privacy_risk():
    assert "data_privacy_risk" in _risk_tags("financial_advisor_copilot")


def test_missing_tool_call_logging_triggers_auditability_gap():
    assert "auditability_gap" in _risk_tags("high_risk_autonomous_agent")


def test_missing_human_approval_triggers_human_oversight_gap():
    assert "human_oversight_gap" in _risk_tags("customer_support_email_agent")


def test_findings_include_rule_ids_and_framework_refs():
    result = assess_workflow(load_demo_workflow("high_risk_autonomous_agent"))

    assert all(finding.rule_id.startswith("AG-RULE-") for finding in result.findings)
    assert any(finding.framework_refs for finding in result.findings)


def test_missing_red_team_testing_triggers_model_risk():
    result = assess_workflow(load_demo_workflow("customer_support_email_agent"))

    assert any(
        finding.risk_tag == "model_risk"
        and any("red-team" in evidence for evidence in finding.evidence)
        for finding in result.findings
    )
