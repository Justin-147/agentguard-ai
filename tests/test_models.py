import pytest
from pydantic import ValidationError

from agentguard.assessment.normalize import load_demo_workflow
from agentguard.models import AgentWorkflow, DataAccessSpec


def test_demo_workflow_loads_as_model():
    workflow = load_demo_workflow("financial_advisor_copilot")

    assert isinstance(workflow, AgentWorkflow)
    assert workflow.id == "financial_advisor_copilot"
    assert workflow.human_oversight.human_in_the_loop is True


def test_data_access_rejects_unknown_sensitivity():
    with pytest.raises(ValidationError):
        DataAccessSpec(
            data_category="unknown",
            sensitivity="secret_plus",
            purpose="Test invalid input.",
            retention_policy_declared=True,
            pii_redaction=True,
            encryption_required=True,
        )
