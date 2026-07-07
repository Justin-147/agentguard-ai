"""Rule-based risk scoring utilities."""

from __future__ import annotations

from statistics import mean

from agentguard.models import AgentWorkflow, RiskFinding

SEVERITY_SCORES = {
    "critical": 1.0,
    "high": 0.8,
    "medium": 0.5,
    "low": 0.25,
}

LIKELIHOOD_SCORES = {
    "high": 0.8,
    "medium": 0.5,
    "low": 0.25,
}

CONTROL_GAP_SCORES = {
    "critical": 1.0,
    "high": 0.75,
    "medium": 0.5,
    "low": 0.25,
}


def calculate_finding_score(finding: RiskFinding) -> float:
    severity_score = SEVERITY_SCORES[finding.severity]
    likelihood_score = LIKELIHOOD_SCORES[finding.likelihood]
    control_gap_score = CONTROL_GAP_SCORES[finding.severity]
    score = 0.45 * severity_score + 0.35 * likelihood_score + 0.20 * control_gap_score
    return round(min(max(score, 0.0), 1.0), 4)


def score_findings(findings: list[RiskFinding]) -> list[RiskFinding]:
    return [
        finding.model_copy(update={"risk_score": calculate_finding_score(finding)})
        for finding in findings
    ]


def calculate_score_explanation(
    findings: list[RiskFinding],
    control_gaps: list[str],
    workflow: AgentWorkflow | None = None,
    top_n: int = 5,
) -> dict[str, float | str]:
    top_scores = sorted((finding.risk_score for finding in findings), reverse=True)[:top_n]
    max_finding_score = max(top_scores) if top_scores else 0.0
    mean_top_5_score = mean(top_scores) if top_scores else 0.0
    control_gap_density = min(1.0, len(control_gaps) / 12)
    score = 0.50 * max_finding_score + 0.30 * mean_top_5_score + 0.20 * control_gap_density
    override = determine_override(workflow, findings) if workflow else "none"
    return {
        "max_finding_score": round(max_finding_score, 4),
        "mean_top_5_score": round(mean_top_5_score, 4),
        "control_gap_density": round(control_gap_density, 4),
        "weighted_score": round(min(max(score, 0.0), 1.0), 4),
        "override_applied": override,
    }


def calculate_overall_score(
    findings: list[RiskFinding],
    control_gaps: list[str] | None = None,
    workflow: AgentWorkflow | None = None,
    top_n: int = 5,
) -> float:
    if control_gaps is None:
        if not findings:
            return 0.0
        top_scores = sorted((finding.risk_score for finding in findings), reverse=True)[:top_n]
        return round(mean(top_scores), 4)
    explanation = calculate_score_explanation(findings, control_gaps, workflow, top_n)
    return float(explanation["weighted_score"])


def determine_override(workflow: AgentWorkflow | None, findings: list[RiskFinding]) -> str:
    if workflow is None:
        return "none"
    financial_action_without_approval = any(
        tool.can_trigger_financial_action and not tool.requires_approval for tool in workflow.tools
    ) or any(
        action.action_type in {"transaction", "payment", "trade", "trading"}
        and not action.requires_human_approval
        for action in workflow.external_actions
    )
    customer_facing_high_impact_without_approval = (
        workflow.deployment.environment == "customer_facing"
        and any(
            action.business_impact == "high" and not action.requires_human_approval
            for action in workflow.external_actions
        )
    )
    sensitive_memory_without_lifecycle = (
        workflow.memory.uses_memory
        and workflow.memory.contains_sensitive_data
        and not (workflow.memory.expiration_policy or workflow.memory.user_deletion_supported)
    )
    no_audit_logging_with_external_action = (
        not workflow.logging.tool_call_logging and bool(workflow.external_actions)
    )
    weak_logging = (
        not workflow.logging.tool_call_logging
        or not workflow.logging.decision_trace
        or not workflow.logging.audit_export_available
    )

    if (
        financial_action_without_approval
        and weak_logging
        and workflow.deployment.environment == "customer_facing"
    ):
        return "critical"
    if any(
        [
            financial_action_without_approval,
            customer_facing_high_impact_without_approval,
            sensitive_memory_without_lifecycle,
            no_audit_logging_with_external_action,
        ]
    ):
        return "high"
    if any(finding.severity == "critical" for finding in findings):
        return "finding-critical"
    return "none"


def determine_overall_risk_level(score: float, override: str = "none") -> str:
    if override == "critical":
        return "Critical"
    if override in {"high", "finding-critical"} and score < 0.55:
        return "High"
    if score < 0.30:
        return "Low"
    if score < 0.55:
        return "Medium"
    if score < 0.75:
        return "High"
    return "Critical"
