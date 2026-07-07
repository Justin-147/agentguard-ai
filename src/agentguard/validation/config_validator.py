"""Validate AgentGuard configuration files."""

from __future__ import annotations

from pathlib import Path

from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.config import (
    config_dir,
    load_control_library,
    load_demo_cases,
    load_framework_mapping,
    load_risk_taxonomy,
    project_root,
    report_template_path,
)
from agentguard.validation.workflow_validator import ValidationIssue

ALLOWED_RISK_NEIGHBORS = {
    "Low": {"Low", "Medium"},
    "Medium": {"Low", "Medium", "High"},
    "High": {"Medium", "High", "Critical"},
    "Critical": {"High", "Critical"},
}


def _issue(level: str, location: str, message: str) -> ValidationIssue:
    return ValidationIssue(level=level, location=location, message=message)


def validate_all_configs() -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    taxonomy = load_risk_taxonomy().get("risk_tags", {})
    controls = load_control_library().get("controls", {})
    demo_cases = load_demo_cases()
    frameworks = load_framework_mapping().get("frameworks", {})

    for risk_tag, config in taxonomy.items():
        if not config.get("description"):
            issues.append(_issue("error", f"risk_taxonomy.{risk_tag}", "description is required."))
        mapped_controls = [
            control_id
            for control_id, control in controls.items()
            if risk_tag in control.get("mitigates", [])
        ]
        if not mapped_controls and not config.get("control_optional"):
            issues.append(
                _issue(
                    "error",
                    f"risk_taxonomy.{risk_tag}",
                    "risk_tag must have at least one mapped control.",
                )
            )

    for control_id, control in controls.items():
        for risk_tag in control.get("mitigates", []):
            if risk_tag not in taxonomy:
                issues.append(
                    _issue(
                        "error",
                        f"control_library.{control_id}",
                        f"Unknown mitigated risk_tag: {risk_tag}.",
                    )
                )

    for framework_id, framework in frameworks.items():
        for risk_tag in framework.get("risk_tags", []):
            if risk_tag not in taxonomy:
                issues.append(
                    _issue(
                        "error",
                        f"framework_mapping.{framework_id}",
                        f"Unknown mapped risk_tag: {risk_tag}.",
                    )
                )

    for case_name, case in demo_cases.items():
        case_path = project_root() / case["path"]
        if not case_path.exists():
            issues.append(
                _issue("error", f"demo_cases.{case_name}", "workflow path does not exist.")
            )
            continue
        expected = case.get("expected_risk")
        result = assess_workflow(load_demo_workflow(case_name))
        allowed = ALLOWED_RISK_NEIGHBORS.get(str(expected), {str(expected)})
        if result.overall_risk_level not in allowed:
            issues.append(
                _issue(
                    "error",
                    f"demo_cases.{case_name}.expected_risk",
                    f"expected {expected}, got {result.overall_risk_level}.",
                )
            )

    template_text = report_template_path().read_text(encoding="utf-8")
    if "Disclaimer" not in template_text:
        issues.append(
            _issue("error", str(report_template_path()), "Report template needs Disclaimer.")
        )

    if not (config_dir() / "rules.yaml").exists():
        issues.append(_issue("error", "config.rules", "rules.yaml is missing."))

    return issues


def validate_config() -> list[ValidationIssue]:
    return validate_all_configs()


def write_issues(issues: list[ValidationIssue]) -> str:
    errors = sum(1 for issue in issues if issue.level == "error")
    warnings = sum(1 for issue in issues if issue.level == "warning")
    lines = [
        f"validation_errors: {errors}",
        f"validation_warnings: {warnings}",
        f"status: {'failed' if errors else 'passed'}",
    ]
    for issue in issues:
        lines.append(f"{issue.level}: {issue.location}: {issue.message}")
    return "\n".join(lines)


def docs_dir() -> Path:
    return project_root() / "docs"
