"""Pure helpers for the Streamlit dashboard."""

from __future__ import annotations

from typing import Any

import pandas as pd

from agentguard.assessment.risk_engine import assess_workflow
from agentguard.models import AgentWorkflow, AssessmentResult, RiskFinding


def findings_to_dataframe(findings: list[RiskFinding]) -> pd.DataFrame:
    rows = [finding.model_dump(mode="json") for finding in findings]
    return pd.DataFrame(rows)


def filter_findings(
    findings: list[RiskFinding],
    *,
    severities: list[str] | None = None,
    risk_tags: list[str] | None = None,
    min_score: float = 0.0,
) -> list[RiskFinding]:
    severity_set = set(severities or [])
    risk_tag_set = set(risk_tags or [])
    filtered: list[RiskFinding] = []
    for finding in findings:
        if severity_set and finding.severity not in severity_set:
            continue
        if risk_tag_set and finding.risk_tag not in risk_tag_set:
            continue
        if finding.risk_score < min_score:
            continue
        filtered.append(finding)
    return filtered


def summarize_case(workflow: AgentWorkflow, result: AssessmentResult) -> dict[str, Any]:
    top_risk_tags: list[str] = []
    for finding in sorted(result.findings, key=lambda item: item.risk_score, reverse=True):
        if finding.risk_tag not in top_risk_tags:
            top_risk_tags.append(finding.risk_tag)
        if len(top_risk_tags) == 3:
            break
    return {
        "case": workflow.id,
        "name": workflow.name,
        "overall_score": result.overall_score,
        "overall_risk_level": result.overall_risk_level,
        "findings_count": len(result.findings),
        "top_risk_tags": ", ".join(top_risk_tags),
    }


def comparison_dataframe(workflows: list[AgentWorkflow]) -> pd.DataFrame:
    rows = [summarize_case(workflow, assess_workflow(workflow)) for workflow in workflows]
    return pd.DataFrame(rows)
