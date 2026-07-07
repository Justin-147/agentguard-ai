import json

from agentguard.validation.workflow_validator import (
    validate_workflow_file,
    validate_workflow_payload,
)


def test_validate_workflow_file_passes_with_warnings_for_high_risk_demo():
    issues = validate_workflow_file("examples/workflows/high_risk_autonomous_agent.json")

    assert not [issue for issue in issues if issue.level == "error"]
    assert [issue for issue in issues if issue.level == "warning"]


def test_invalid_workflow_returns_error(tmp_path):
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text(json.dumps({"id": "", "tools": []}), encoding="utf-8")

    issues = validate_workflow_file(invalid_path)

    assert [issue for issue in issues if issue.level == "error"]


def test_duplicate_tool_name_returns_error():
    payload = {
        "id": "duplicate_tool",
        "name": "Duplicate Tool",
        "description": "Invalid duplicate tool workflow.",
        "business_domain": "test",
        "agent_type": "test_agent",
        "tools": [
            {
                "name": "reader",
                "tool_type": "filesystem",
                "description": "Read",
                "permissions": ["read"],
            },
            {
                "name": "reader",
                "tool_type": "filesystem",
                "description": "Read again",
                "permissions": ["read"],
            },
        ],
        "data_access": [],
        "external_actions": [],
        "human_oversight": {
            "human_in_the_loop": True,
            "approval_required_for_high_risk_actions": True,
            "review_frequency": "weekly",
            "escalation_path_defined": True,
        },
        "logging": {
            "tool_call_logging": True,
            "input_output_logging": False,
            "decision_trace": True,
            "retention_days": 30,
            "audit_export_available": True,
        },
        "memory": {
            "uses_memory": False,
            "memory_type": "none",
            "contains_sensitive_data": False,
            "expiration_policy": True,
            "user_deletion_supported": True,
        },
        "evaluation": {
            "pre_deployment_tests": True,
            "ongoing_monitoring": True,
            "red_team_testing": True,
            "hallucination_tests": True,
            "prompt_injection_tests": True,
            "fallback_tests": True,
        },
        "deployment": {
            "environment": "local",
            "rate_limits": True,
            "secrets_management": True,
            "incident_response_plan": True,
            "rollback_plan": True,
        },
    }

    issues = validate_workflow_payload(payload)

    assert any(issue.level == "error" and "Duplicate" in issue.message for issue in issues)
