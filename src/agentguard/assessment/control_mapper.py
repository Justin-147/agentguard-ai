"""Map risk findings to governance controls."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from agentguard.config import load_control_library
from agentguard.models import AgentWorkflow, RiskFinding


def _controls(library: dict[str, Any] | None = None) -> dict[str, Any]:
    return (library or load_control_library()).get("controls", {})


def controls_for_risk_tag(
    risk_tag: str, library: dict[str, Any] | None = None
) -> list[str]:
    matched: list[str] = []
    for control_id, control in _controls(library).items():
        if risk_tag in control.get("mitigates", []):
            matched.append(control_id)
    return matched


def attach_recommended_controls(
    findings: Iterable[RiskFinding], library: dict[str, Any] | None = None
) -> list[RiskFinding]:
    enriched: list[RiskFinding] = []
    for finding in findings:
        controls = controls_for_risk_tag(finding.risk_tag, library)
        enriched.append(finding.model_copy(update={"recommended_controls": controls}))
    return enriched


def control_description(
    control_id: str, library: dict[str, Any] | None = None
) -> str:
    return _controls(library).get(control_id, {}).get("description", "")


def unique_controls_from_findings(findings: Iterable[RiskFinding]) -> list[str]:
    controls: list[str] = []
    for finding in findings:
        for control_id in finding.recommended_controls:
            if control_id not in controls:
                controls.append(control_id)
    return controls


def identify_control_gaps(
    workflow: AgentWorkflow, findings: Iterable[RiskFinding]
) -> list[str]:
    gaps = unique_controls_from_findings(findings)

    def add(control_id: str) -> None:
        if control_id not in gaps:
            gaps.append(control_id)

    if any(
        access.sensitivity in {"personal", "financial", "regulated", "confidential"}
        and not access.retention_policy_declared
        for access in workflow.data_access
    ):
        add("retention_policy")

    if any(
        access.sensitivity in {"personal", "financial", "regulated", "confidential"}
        and not access.pii_redaction
        for access in workflow.data_access
    ):
        add("pii_redaction")

    if not workflow.logging.tool_call_logging:
        add("tool_call_audit_log")

    if not workflow.human_oversight.approval_required_for_high_risk_actions:
        add("human_approval_gate")

    if not workflow.evaluation.prompt_injection_tests:
        add("prompt_injection_tests")

    if not (
        workflow.evaluation.pre_deployment_tests
        and workflow.evaluation.hallucination_tests
    ):
        add("evaluation_suite")

    if not workflow.evaluation.fallback_tests:
        add("fallback_procedure")

    if not workflow.deployment.incident_response_plan:
        add("incident_response_plan")

    if not workflow.deployment.secrets_management:
        add("secrets_management")

    if not workflow.deployment.rate_limits:
        add("rate_limits")

    return gaps
