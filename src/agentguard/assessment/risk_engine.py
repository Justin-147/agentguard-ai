"""Deterministic workflow risk engine."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from agentguard.assessment.control_mapper import (
    attach_recommended_controls,
    identify_control_gaps,
)
from agentguard.assessment.recommendations import (
    build_recommendations,
    identify_strengths,
)
from agentguard.assessment.scoring import (
    calculate_score_explanation,
    determine_overall_risk_level,
    score_findings,
)
from agentguard.config import load_rules
from agentguard.models import AgentWorkflow, AssessmentResult, RiskFinding

SENSITIVE_DATA = {"personal", "financial", "regulated", "confidential"}

UNTRUSTED_PATTERNS = {
    "email": [r"\bemail\b", r"\bmailbox\b", r"\boutbound mail\b"],
    "web": [r"\bweb\b", r"\binternet\b", r"\bpublic sources?\b", r"\bpublic web\b"],
    "uploaded_document": [
        r"\buploaded document\b",
        r"\buser uploaded\b",
        r"\bexternal document\b",
    ],
    "customer_message": [
        r"\bcustomer message\b",
        r"\bcustomer_messages\b",
        r"\bsupport request\b",
    ],
    "ticket": [r"\bsupport ticket\b", r"\bticket\b", r"\bticketing system\b"],
    "external_api": [r"\bexternal api\b", r"\bapi_call\b", r"\bthird[- ]party api\b"],
}


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ").replace("-", " ").lower())


def _workflow_text(workflow: AgentWorkflow) -> str:
    text_parts = [workflow.description, workflow.business_domain, workflow.agent_type]
    text_parts.extend(tool.name for tool in workflow.tools)
    text_parts.extend(tool.description for tool in workflow.tools)
    text_parts.extend(tool.tool_type for tool in workflow.tools)
    text_parts.extend(access.data_category for access in workflow.data_access)
    text_parts.extend(action.action_type for action in workflow.external_actions)
    text_parts.extend(action.description for action in workflow.external_actions)
    return _normalize_text(" ".join(text_parts))


def detect_untrusted_input_sources(workflow: AgentWorkflow) -> list[str]:
    """Return normalized untrusted input sources detected in workflow metadata."""

    text = _workflow_text(workflow)
    sources: list[str] = []
    for source, patterns in UNTRUSTED_PATTERNS.items():
        if any(re.search(pattern, text) for pattern in patterns):
            sources.append(source)

    if any(tool.tool_type.lower() == "api" for tool in workflow.tools) or any(
        action.action_type == "api_call" for action in workflow.external_actions
    ):
        if "external_api" not in sources:
            sources.append("external_api")
    return sources


class FindingBuilder:
    def __init__(self, rules: dict[str, Any] | None = None) -> None:
        self._items: list[RiskFinding] = []
        self._rules = rules or load_rules()

    def add(
        self,
        rule_id: str,
        severity: str,
        likelihood: str,
        affected_component: str,
        evidence: list[str],
        *,
        risk_tag: str | None = None,
        title: str | None = None,
        description: str | None = None,
        recommended_controls: list[str] | None = None,
        framework_refs: list[str] | None = None,
    ) -> None:
        rule = self._rules.get(rule_id, {})
        finding_id = f"AGF-{len(self._items) + 1:03d}"
        controls = list(rule.get("base_controls", []))
        for control_id in recommended_controls or []:
            if control_id not in controls:
                controls.append(control_id)
        self._items.append(
            RiskFinding(
                id=finding_id,
                rule_id=rule_id,
                risk_tag=risk_tag or rule.get("risk_tag", "operational_risk"),
                title=title or rule.get("title", "Risk finding"),
                description=description
                or rule.get("description", "A workflow risk was identified."),
                severity=severity,
                likelihood=likelihood,
                risk_score=0.0,
                affected_component=affected_component,
                evidence=evidence,
                recommended_controls=controls,
                framework_refs=framework_refs or list(rule.get("framework_refs", [])),
            )
        )

    def findings(self) -> list[RiskFinding]:
        return self._items


def _has_sensitive_data(workflow: AgentWorkflow) -> bool:
    return any(access.sensitivity in SENSITIVE_DATA for access in workflow.data_access)


def _has_high_impact_action(workflow: AgentWorkflow) -> bool:
    return any(action.business_impact == "high" for action in workflow.external_actions)


def generate_risk_findings(workflow: AgentWorkflow) -> list[RiskFinding]:
    builder = FindingBuilder()
    untrusted_sources = detect_untrusted_input_sources(workflow)
    has_sensitive_data = _has_sensitive_data(workflow)

    for action in workflow.external_actions:
        if not action.requires_human_approval and action.business_impact in {"medium", "high"}:
            severity = "high" if action.business_impact == "high" else "medium"
            likelihood = (
                "high"
                if action.action_type in {"transaction", "email", "api_call"}
                else "medium"
            )
            builder.add(
                "AG-RULE-ACTION-001",
                severity,
                likelihood,
                f"external_action:{action.action_type}",
                [
                    (
                        f"Action '{action.action_type}' has business impact "
                        f"'{action.business_impact}'."
                    ),
                    "requires_human_approval is false.",
                ],
            )
            builder.add(
                "AG-RULE-HUMAN-001",
                severity,
                "medium",
                f"external_action:{action.action_type}",
                [
                    f"Action '{action.action_type}' can run without human approval.",
                    f"Workflow review frequency is '{workflow.human_oversight.review_frequency}'.",
                ],
            )

        if action.business_impact == "high" and not action.reversible:
            builder.add(
                "AG-RULE-OPS-001",
                "high",
                "medium",
                f"external_action:{action.action_type}",
                [
                    f"Action '{action.action_type}' is high impact.",
                    "reversible is false.",
                ],
            )

    if _has_high_impact_action(workflow) and not workflow.human_oversight.escalation_path_defined:
        builder.add(
            "AG-RULE-HUMAN-001",
            "high",
            "medium",
            "human_oversight",
            [
                "At least one external action has high business impact.",
                "escalation_path_defined is false.",
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
            severity = (
                "high"
                if access.sensitivity == "regulated"
                or (both_missing and workflow.memory.contains_sensitive_data)
                else "medium"
            )
            likelihood = "high" if both_missing else "medium"
            builder.add(
                "AG-RULE-DATA-001",
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
                    "AG-RULE-REG-001",
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
                "AG-RULE-CYBER-001",
                "medium",
                "medium",
                f"data_access:{access.data_category}",
                [
                    f"Data category '{access.data_category}' is '{access.sensitivity}'.",
                    "encryption_required is false.",
                ],
                title="Sensitive data encryption is not required",
            )

        if (
            workflow.logging.input_output_logging
            and access.sensitivity in SENSITIVE_DATA
            and not access.pii_redaction
        ):
            builder.add(
                "AG-RULE-DATA-001",
                "medium",
                "medium",
                f"logging:{access.data_category}",
                [
                    "input_output_logging is true for a workflow with sensitive data.",
                    f"Data category '{access.data_category}' has pii_redaction=false.",
                ],
                title="Input/output logs may capture unredacted sensitive data",
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
                "AG-RULE-TOOL-001",
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
                    "AG-RULE-ACTION-001",
                    "critical" if tool.can_trigger_financial_action else "high",
                    "high",
                    f"tool:{tool.name}",
                    [
                        (
                            f"Tool '{tool.name}' can send external messages or trigger "
                            "financial action."
                        ),
                        "requires_approval is false.",
                    ],
                    title="Tool can trigger external impact",
                )

            if tool.can_execute or tool.can_trigger_financial_action:
                builder.add(
                    "AG-RULE-CYBER-001",
                    severity,
                    "medium",
                    f"tool:{tool.name}",
                    [
                        f"Tool '{tool.name}' exposes privileged permissions.",
                        f"Declared permissions: {', '.join(tool.permissions)}.",
                    ],
                    title="Privileged tool execution risk",
                )

    audit_gaps = []
    if not workflow.logging.tool_call_logging:
        audit_gaps.append("tool-call logging")
    if not workflow.logging.input_output_logging and has_sensitive_data:
        audit_gaps.append("input/output logging for sensitive-data workflow")
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
            "AG-RULE-AUDIT-001",
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
    if not workflow.evaluation.red_team_testing and (
        workflow.external_actions or untrusted_sources
    ):
        missing_evaluations.append("red-team tests for agent/tool abuse")
    if not workflow.evaluation.hallucination_tests:
        missing_evaluations.append("hallucination tests")
    if not workflow.evaluation.fallback_tests:
        missing_evaluations.append("fallback tests")
    if missing_evaluations:
        severity = "medium" if len(missing_evaluations) >= 2 else "low"
        if (
            "red-team tests for agent/tool abuse" in missing_evaluations
            and workflow.external_actions
        ):
            severity = "high"
        builder.add(
            "AG-RULE-MODEL-001",
            severity,
            "medium",
            "evaluation",
            [f"Missing evaluation control: {item}." for item in missing_evaluations],
        )

        if "ongoing monitoring" in missing_evaluations or "fallback tests" in missing_evaluations:
            builder.add(
                "AG-RULE-OPS-001",
                "medium" if len(missing_evaluations) >= 2 else "low",
                "medium",
                "evaluation",
                [f"Missing evaluation control: {item}." for item in missing_evaluations],
                title="Operational monitoring or fallback is incomplete",
            )

    if untrusted_sources and not workflow.evaluation.prompt_injection_tests:
        severity = "high" if workflow.external_actions else "medium"
        builder.add(
            "AG-RULE-PROMPT-001",
            severity,
            "medium",
            "evaluation",
            [
                f"Untrusted input sources detected: {', '.join(untrusted_sources)}.",
                "prompt_injection_tests is false.",
            ],
        )
        builder.add(
            "AG-RULE-CYBER-001",
            severity,
            "medium",
            "evaluation",
            [
                f"Untrusted input sources detected: {', '.join(untrusted_sources)}.",
                "Prompt-injection testing is not declared.",
            ],
            title="Prompt injection can affect tool use",
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
            "AG-RULE-OPS-001",
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
            "AG-RULE-CYBER-001",
            "high",
            "medium",
            "deployment",
            [
                "secrets_management is false.",
                "Workflow includes API, execution, external-send, or transaction-capable tools.",
            ],
            title="Secrets management is missing for privileged tools",
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
            "AG-RULE-MEMORY-001",
            "high",
            "high",
            "memory",
            [
                f"memory_type is '{workflow.memory.memory_type}'.",
                *[f"Missing memory control: {item}." for item in missing_memory_controls],
            ],
        )

    if workflow.memory.memory_type == "vector_store" and workflow.memory.contains_sensitive_data:
        builder.add(
            "AG-RULE-MEMORY-001",
            "high",
            "medium",
            "memory",
            [
                "memory_type is 'vector_store'.",
                "contains_sensitive_data is true.",
            ],
            title="Sensitive vector memory needs access controls",
        )
        builder.add(
            "AG-RULE-PROMPT-001",
            "medium",
            "medium",
            "memory",
            [
                "Vector memory can retrieve untrusted or stale context.",
                "contains_sensitive_data is true.",
            ],
            title="Sensitive vector memory can amplify prompt-injection risk",
        )

    has_api_dependency = any(tool.tool_type.lower() == "api" for tool in workflow.tools) or any(
        action.action_type == "api_call" for action in workflow.external_actions
    )
    if has_api_dependency:
        builder.add(
            "AG-RULE-THIRD-001",
            "medium",
            "medium",
            "tools",
            ["Workflow includes an API tool or API-call external action."],
        )

    return builder.findings()


def assess_workflow(
    workflow: AgentWorkflow, generated_at: datetime | None = None
) -> AssessmentResult:
    findings = generate_risk_findings(workflow)
    findings = attach_recommended_controls(findings)
    findings = score_findings(findings)
    control_gaps = identify_control_gaps(workflow, findings)
    recommendations = build_recommendations(workflow, findings, control_gaps)
    strengths = identify_strengths(workflow)
    score_explanation = calculate_score_explanation(findings, control_gaps, workflow)
    overall_score = float(score_explanation["weighted_score"])
    overall_risk_level = determine_overall_risk_level(
        overall_score,
        str(score_explanation["override_applied"]),
    )
    return AssessmentResult(
        workflow_id=workflow.id,
        workflow_name=workflow.name,
        overall_risk_level=overall_risk_level,
        overall_score=overall_score,
        findings=findings,
        control_gaps=control_gaps,
        strengths=strengths,
        recommendations=recommendations,
        score_explanation=score_explanation,
        generated_at=generated_at or datetime.now(UTC),
    )
