from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.assessment.scoring import determine_overall_risk_level


def test_overall_score_is_between_zero_and_one():
    result = assess_workflow(load_demo_workflow("high_risk_autonomous_agent"))

    assert 0.0 <= result.overall_score <= 1.0
    assert all(0.0 <= finding.risk_score <= 1.0 for finding in result.findings)


def test_score_thresholds_match_expected_levels():
    assert determine_overall_risk_level(0.10) == "Low"
    assert determine_overall_risk_level(0.40) == "Medium"
    assert determine_overall_risk_level(0.60) == "High"
    assert determine_overall_risk_level(0.90) == "Critical"
