from agentguard.config import load_demo_cases
from agentguard.validation.config_validator import validate_config


def test_config_validation_passes():
    issues = validate_config()

    assert not [issue for issue in issues if issue.level == "error"]


def test_all_demo_expected_risk_is_in_allowed_range():
    issues = validate_config()
    messages = [issue.message for issue in issues]

    assert load_demo_cases()
    assert not any("expected" in message and "got" in message for message in messages)
