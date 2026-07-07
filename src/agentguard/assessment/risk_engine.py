"""Deterministic workflow risk engine."""

from __future__ import annotations

from datetime import datetime, timezone

from agentguard.assessment.control_mapper import (
    attach_recommended_controls,
    identify_control_gaps,
)
from agentguard.assessment.recommendations import (
    build_recommendations,
    identify_strengths,
)
from agentguard.assessment.scoring import (
    calculate_overall_score,
    determine_overall_risk_level,
    score_findings,
)
from agentguard.models import AgentWorkflow, AssessmentResult, RiskFinding


SENSITIVE_DATA = {"personal", "financial", "regulated", "confidential"}
UNTRUSTED_TERMS = {
    "email",
    "web",
    "internet",
    "external",
    "uploaded document",
    "outside user",
    "customer message",
    "customer_messages",
    "ticket",
    "support request",
}


class FindingBuilder:
    def __init__(self) -> None:
        self._items: list[RiskFinding] = []

    def add(
        self,
        risk_tag: str,
        title: str,
        description: str,
        severity: str,
        likelihood: str,
        affected_component: str,
        evidence: list[str],
    ) -> None:
        finding_id = f"AGF-{len(self._items) + 1:03d}"
        self._items.append(
            RiskFinding(
                id=finding_id,
                risk_tag=risk_tag,
                title=title,
                description=description,
                severity=severity,
                likelihood=likelihood,
                risk_score=0.0,
                affected_component=affected_component,
                evidence=evidence,
                recommended_controls=[],
            )
        )

    def findings(self) -> list[RiskFinding]:
        return self._items


def _has_untrusted_inputs(workflow: AgentWorkflow) -> bool:
    text_parts = [
        workflow.description,
        workflow.business_domain,
        workflow.agent_type,
    ]
    text_parts.extend(tool.description for tool in workflow.tools)
    text_parts.extend(tool.tool_type for tool in workflow.tools)
    text_parts.extend(access.data_category for access in workflow.data_access)
    text_parts.extend(action.action_type for action in workflow.external_actions)
    text_parts.extend(action.description for action in workflow.external_actions)
    combined = " ".join(text_parts).lower()
    return any(term in combined for term in UNTRUSTED_TERMS)


def generate_risk_findings(workflow: AgentWorkflow) -> list[RiskFinding]:
    builder = FindingBuilder()

    for action in workflow.external_actions:
        if (
            not action.requires_human_approval
            and action.business_impact in {"medium", "high"}
        ):
            severity = "high" if action.business_impact == "high" else "medium"
            likelihood = "high" if action.action_type in {"transaction", "email", "api_call"} else "medium"
            builder.add(
                "external_action_risk",
                "External action lacks approval",
                "The agent can take an outward-facing or business-impacting action without a human approval gate.",
                severity,
                likelihood,
                f"external_action:{action.action_type}",
                [
                    f"Action '{action.action_type}' has business impact '{action.business_impact}'.",
                    "requires_human_approval is false.",
                ],
            )
            builder.add(
                "human_oversight_gap",
                "Approval gap for external action",
                "Medium or high impact agent actions should have explicit review or approval before execution.",
                severity,
                "medium",
                f"external_action:{action.action_type}",
                [
                    f"Action '{action.action_type}' can run without human approval.",
                    f"Workflow review frequency is '{workflow.human_oversight.review_frequency}'.",
                ],
            )

    for access in workflow.data_access:
        if access.sensitivity in SENSITIVE_DATA and (
            not access.retention_policy_declared or not access.pii_redaction
        ):
            missing = []
            if not access.retention_policy_declared:
                missing.append("retention policy")
            if not access.pii_redaction:
                missing.append("PII redaction")
            both_missing = len(missing) == 2
            severity = "high" if access.sensitivity == "regulated" or (
                both_missing and workflow.memory.contains_sensitive_data
            ) else "medium"
            likelihood = "high" if both_missing else "medium"
            builder.add(
                "data_privacy_risk",
                "Sensitive data controls are incomplete",
                "Sensitive data processing lacks one or more basic privacy controls.",
                severity,
                likelihood,
                f"data_access:{access.data_category}",
                [
                    f"Data category '{access.data_category}' is marked '{access.sensitivity}'.",
                    f"Missing: {', '.join(missing)}.",
                ],
            )

            if access.sensitivity in {"financial", "regulated"}:
                builder.add(
                    "regulatory_risk",
                    "Regulated or financial data exposure",
                    "Financial or regulated data increases the need for controlled records, monitoring, and review.",
                    "medium" if severity == "medium" else "high",
                    "medium" if access.sensitivity == "regulated" else "low",
                    f"data_access:{access.data_category}",
                    [
                        f"Data sensitivity is '{access.sensitivity}'.",
                        f"Privacy controls missing: {', '.join(missing)}.",
                    ],
                )

        if access.sensitivity in SENSITIVE_DATA and not access.encryption_required:
            builder.add(
                "cybersecurity_risk",
                "Sensitive data encryption is not required",
                "Sensitive or confidential data should have explicit encryption requirements.",
                "medium",
                "medium",
                f"data_access:{access.data_category}",
                [
                    f"Data category '{access.data_category}' is '{access.sensitivity}'.",
                    "encryption_required is false.",
                ],
            )

    for tool in workflow.tools:
        dangerous_permissions = [
            label
            for label, active in {
                "write": tool.can_write,
                "execute": tool.can_execute,
                "send_external_message": tool.can_send_external_message,
                "trigger_financial_action": tool.can_trigger_financial_action,
            }.items()
            if active
        ]
        if dangerous_permissions and not tool.requires_approval:
            severity = "critical" if tool.can_trigger_financial_action else "high"
            if tool.can_write and not (tool.can_execute or tool.can_send_external_message):
                severity = "medium"
            likelihood = "high" if tool.can_execute or tool.can_send_external_message else "medium"
            builder.add(
                "tool_permission_risk",
                "Tool permission is not approval-gated",
                "The workflow gives the agent broad or potentially dangerous tool permissions without approval.",
                severity,
                likelihood,
                f"tool:{tool.name}",
                [
                    f"Tool '{tool.name}' has permissions: {', '.join(dangerous_permissions)}.",
                    "requires_approval is false.",
                ],
            )

            if tool.can_send_external_message or tool.can_trigger_financial_action:
                builder.add(
                    "external_action_risk",
                    "Tool can trigger external impact",
                    "A tool permission can create outward-facing or business-impacting effects without approval.",
                    "critical" if tool.can_trigger_financial_action else "high",
                    "high",
                    f"tool:{tool.name}",
                    [
                        f"Tool '{tool.name}' can send external messages or trigger financial action.",
                        "requires_approval is false.",
                    ],
                )

            if tool.can_execute or tool.can_trigger_financial_action:
                builder.add(
                    "cybersecurity_risk",
                    "Privileged tool execution risk",
                    "Execute or transaction-capable tools increase security and access-control risk.",
                    severity,
                    "medium",
                    f"tool:{tool.name}",
                    [
                        f"Tool '{tool.name}' exposes privileged permissions.",
                        f"Declared permissions: {', '.join(tool.permissions)}.",
                    ],
                )

    audit_gaps = []
    if not workflow.logging.tool_call_logging:
        audit_gaps.append("tool-call logging")
    if not workflow.logging.decision_trace:
        audit_gaps.append("decision trace")
    if not workflow.logging.audit_export_available:
        audit_gaps.append("audit export")
    if workflow.logging.retention_days is None:
        audit_gaps.append("log retention period")
    if audit_gaps:
        severity = "high" if len(audit_gaps) >= 3 else "medium"
        likelihood = "high" if len(audit_gaps) >= 3 else "medium"
        builder.add(
            "auditability_gap",
            "Audit trail is incomplete",
            "The workflow may be difficult to investigate, replay, or evidence during governance review.",
            severity,
            likelihood,
            "logging",
            [f"Missing audit feature: {gap}." for gap in audit_gaps],
        )

    missing_evaluations = []
    if not workflow.evaluation.pre_deployment_tests:
        missing_evaluations.append("pre-deployment tests")
    if not workflow.evaluation.ongoing_monitoring:
        missing_evaluations.append("ongoing monitoring")
    if not workflow.evaluation.hallucination_tests:
        missing_evaluations.append("hallucination tests")
    if not workflow.evaluation.fallback_tests:
        missing_evaluations.append("fallback tests")
    if missing_evaluations:
        severity = "medium" if len(missing_evaluations) >= 2 else "low"
        likelihood = "medium"
        builder.add(
            "model_risk",
            "Model evaluation coverage is incomplete",
            "The workflow has missing model quality, hallucination, monitoring, or fallback checks.",
            severity,
            likelihood,
            "evaluation",
            [f"Missing evaluation control: {item}." for item in missing_evaluations],
        )

        if (
            "ongoing monitoring" in missing_evaluations
            or "fallback tests" in missing_evaluations
        ):
            builder.add(
                "operational_risk",
                "Operational monitoring or fallback is incomplete",
                "Missing fallback and monitoring controls can delay detection or recovery when the agent fails.",
                "medium" if len(missing_evaluations) >= 2 else "low",
                "medium",
                "evaluation",
                [f"Missing evaluation control: {item}." for item in missing_evaluations],
            )

    if _has_untrusted_inputs(workflow) and not workflow.evaluation.prompt_injection_tests:
        severity = "high" if workflow.external_actions else "medium"
        builder.add(
            "prompt_injection_risk",
            "Untrusted content lacks prompt-injection testing",
            "Agents that read emails, web content, uploaded documents, or customer messages need direct and indirect prompt-injection tests.",
            severity,
            "medium",
            "evaluation",
            [
                "Workflow appears to process untrusted external content.",
                "prompt_injection_tests is false.",
            ],
        )
        builder.add(
            "cybersecurity_risk",
            "Prompt injection can affect tool use",
            "Prompt injection can cause data leakage, unsafe tool use, or unauthorized external actions.",
            severity,
            "medium",
            "evaluation",
            [
                "Untrusted content is in scope.",
                "Prompt-injection testing is not declared.",
            ],
        )

    deployment_gaps = []
    if not workflow.deployment.incident_response_plan:
        deployment_gaps.append("incident response plan")
    if not workflow.deployment.rollback_plan:
        deployment_gaps.append("rollback plan")
    if not workflow.deployment.rate_limits:
        deployment_gaps.append("rate limits")
    if deployment_gaps:
        severity = "high" if workflow.deployment.environment == "customer_facing" else "medium"
        builder.add(
            "operational_risk",
            "Deployment resilience controls are incomplete",
            "Production-like agent deployments need operational limits, rollback, and incident-response readiness.",
            severity,
            "medium",
            "deployment",
            [f"Missing deployment control: {gap}." for gap in deployment_gaps],
        )

    if not workflow.deployment.secrets_management and any(
        tool.can_execute
        or tool.can_send_external_message
        or tool.can_trigger_financial_action
        or tool.tool_type.lower() == "api"
        for tool in workflow.tools
    ):
        builder.add(
            "cybersecurity_risk",
            "Secrets management is missing for privileged tools",
            "Privileged tools and external APIs should use managed secrets rather than ad hoc credentials.",
            "high",
            "medium",
            "deployment",
            [
                "secrets_management is false.",
                "Workflow includes API, execution, external-send, or transaction-capable tools.",
            ],
        )

    if workflow.memory.uses_memory and workflow.memory.contains_sensitive_data and (
        not workflow.memory.expiration_policy or not workflow.memory.user_deletion_supported
    ):
        missing_memory_controls = []
        if not workflow.memory.expiration_policy:
            missing_memory_controls.append("memory expiration policy")
        if not workflow.memory.user_deletion_supported:
            missing_memory_controls.append("user deletion support")
        builder.add(
            "data_privacy_risk",
            "Sensitive memory controls are incomplete",
            "Long-lived memory that contains sensitive data should support expiration and deletion.",
            "high",
            "high",
            "memory",
            [f"Missing memory control: {item}." for item in missing_memory_controls],
        )

    has_api_dependency = any(
        tool.tool_type.lower() == "api" for tool in workflow.tools
    ) or any(action.action_type == "api_call" for action in workflow.external_actions)
    if has_api_dependency:
        builder.add(
            "third_party_risk",
            "External API dependency is present",
            "External providers and APIs introduce availability, data handling, and vendor-control considerations.",
            "medium",
            "medium",
            "tools",
            ["Workflow includes an API tool or API-call external action."],
        )

    return builder.findings()


def assess_workflow(workflow: AgentWorkflow) -> AssessmentResult:
    findings = generate_risk_findings(workflow)
    findings = attach_recommended_controls(findings)
    findings = score_findings(findings)
    control_gaps = identify_control_gaps(workflow, findings)
    recommendations = build_recommendations(workflow, findings, control_gaps)
    strengths = identify_strengths(workflow)
    overall_score = calculate_overall_score(findings)
    overall_risk_level = determine_overall_risk_level(overall_score)
    return AssessmentResult(
        workflow_id=workflow.id,
        workflow_name=workflow.name,
        overall_risk_level=overall_risk_level,
        overall_score=overall_score,
        findings=findings,
        control_gaps=control_gaps,
        strengths=strengths,
        recommendations=recommendations,
        generated_at=datetime.now(timezone.utc),
    )
