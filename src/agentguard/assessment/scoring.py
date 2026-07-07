"""Rule-based risk scoring utilities."""

from __future__ import annotations

from statistics import mean

from agentguard.models import RiskFinding


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
    score = (
        0.45 * severity_score
        + 0.35 * likelihood_score
        + 0.20 * control_gap_score
    )
    return round(min(max(score, 0.0), 1.0), 4)


def score_findings(findings: list[RiskFinding]) -> list[RiskFinding]:
    return [
        finding.model_copy(update={"risk_score": calculate_finding_score(finding)})
        for finding in findings
    ]


def calculate_overall_score(findings: list[RiskFinding], top_n: int = 5) -> float:
    if not findings:
        return 0.0
    top_scores = sorted((finding.risk_score for finding in findings), reverse=True)[:top_n]
    return round(mean(top_scores), 4)


def determine_overall_risk_level(score: float) -> str:
    if score < 0.30:
        return "Low"
    if score < 0.55:
        return "Medium"
    if score < 0.75:
        return "High"
    return "Critical"
