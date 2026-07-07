"""Generate human-readable mitigation recommendations."""

from __future__ import annotations

from agentguard.models import AgentWorkflow, RiskFinding


CONTROL_RECOMMENDATIONS = {
    "human_approval_gate": "Add a human approval gate before high-impact external actions such as outbound messages, API calls, file changes, or transactions.",
    "tool_allowlist": "Restrict the agent to an allowlist of approved tools and permissions that match the workflow's business purpose.",
    "tool_call_audit_log": "Enable tool-call audit logging with timestamp, tool name, input summary, output summary, and execution status.",
    "pii_redaction": "Redact or mask personal and financial identifiers before model processing or long-term storage.",
    "retention_policy": "Define and enforce a retention policy for inputs, outputs, logs, and memory records.",
    "prompt_injection_tests": "Add direct and indirect prompt-injection tests for untrusted emails, web pages, uploaded documents, and customer messages.",
    "evaluation_suite": "Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.",
    "fallback_procedure": "Define fallback behavior for low-confidence outputs, tool failures, and missing evidence.",
    "incident_response_plan": "Document an incident response process for data leakage, harmful tool use, and incorrect external actions.",
    "secrets_management": "Store API keys and credentials in a secrets manager or environment-managed secret store.",
    "rate_limits": "Apply rate limits to constrain the frequency and volume of automated agent actions.",
    "source_attribution": "Require source attribution for factual claims in generated reports or customer-facing content.",
}


def build_recommendations(
    workflow: AgentWorkflow, findings: list[RiskFinding], control_gaps: list[str]
) -> list[str]:
    recommendations: list[str] = []

    def add(text: str) -> None:
        if text and text not in recommendations:
            recommendations.append(text)

    for finding in findings:
        if finding.risk_tag == "external_action_risk":
            add(
                f"Review the '{finding.affected_component}' action path and require approval when business impact is medium or high."
            )
        if finding.risk_tag == "data_privacy_risk":
            add(
                "Classify sensitive input fields, redact personal data where possible, and document retention for each data category."
            )
        if finding.risk_tag == "auditability_gap":
            add(
                "Make assessment replay possible by retaining tool-call logs, decision traces, and exportable audit records."
            )
        if finding.risk_tag == "tool_permission_risk":
            add(
                "Split read, write, execute, and external-send permissions into separately approved tool scopes."
            )

    for control_id in control_gaps:
        add(CONTROL_RECOMMENDATIONS.get(control_id, ""))

    if (
        workflow.business_domain.lower() in {"finance", "financial services", "wealth management"}
        and "source_attribution" not in control_gaps
    ):
        add("Require source attribution for financial summaries and portfolio-related factual claims.")

    return recommendations


def identify_strengths(workflow: AgentWorkflow) -> list[str]:
    strengths: list[str] = []

    if workflow.human_oversight.human_in_the_loop:
        strengths.append("Human-in-the-loop review is enabled.")
    if workflow.human_oversight.approval_required_for_high_risk_actions:
        strengths.append("High-risk actions require approval.")
    if workflow.logging.tool_call_logging:
        strengths.append("Tool-call logging is enabled.")
    if workflow.logging.audit_export_available:
        strengths.append("Audit export is available.")
    if workflow.evaluation.pre_deployment_tests:
        strengths.append("Pre-deployment tests are defined.")
    if workflow.evaluation.ongoing_monitoring:
        strengths.append("Ongoing monitoring is enabled.")
    if workflow.deployment.secrets_management:
        strengths.append("Secrets management is declared.")
    if workflow.deployment.incident_response_plan:
        strengths.append("Incident response planning is declared.")
    if not workflow.external_actions:
        strengths.append("No external actions are configured.")

    return strengths
