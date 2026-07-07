from agentguard.assessment.control_mapper import controls_for_risk_tag
from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.risk_engine import assess_workflow


def test_controls_are_mapped_from_control_library():
    controls = controls_for_risk_tag("data_privacy_risk")

    assert "pii_redaction" in controls
    assert "retention_policy" in controls


def test_recommendations_include_relevant_controls():
    result = assess_workflow(load_demo_workflow("customer_support_email_agent"))

    assert "human_approval_gate" in result.control_gaps
    assert any("approval gate" in item.lower() for item in result.recommendations)
