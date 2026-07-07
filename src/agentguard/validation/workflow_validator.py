"""Validate workflow JSON before model assessment."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agentguard.models import AgentWorkflow, DataAccessSpec, DeploymentSpec, ExternalActionSpec


@dataclass(frozen=True)
class ValidationIssue:
    level: str
    location: str
    message: str


REQUIRED_FIELDS = {
    "id",
    "name",
    "description",
    "business_domain",
    "agent_type",
    "tools",
    "data_access",
    "external_actions",
    "human_oversight",
    "logging",
    "memory",
    "evaluation",
    "deployment",
}


def _issue(level: str, location: str, message: str) -> ValidationIssue:
    return ValidationIssue(level=level, location=location, message=message)


def _is_sensitive(value: str | None) -> bool:
    return value in {"personal", "financial", "regulated", "confidential"}


def validate_workflow_payload(payload: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    missing = sorted(REQUIRED_FIELDS - set(payload))
    for field in missing:
        issues.append(_issue("error", field, "Required field is missing."))

    for field in ("id", "name", "description"):
        if field in payload and not str(payload.get(field) or "").strip():
            issues.append(_issue("error", field, "Field must not be empty."))

    tools = payload.get("tools") or []
    if isinstance(tools, list):
        names = [tool.get("name") for tool in tools if isinstance(tool, dict)]
        duplicates = sorted({name for name in names if name and names.count(name) > 1})
        for name in duplicates:
            issues.append(_issue("error", "tools", f"Duplicate tool name: {name}."))
        for index, tool in enumerate(tools):
            if not isinstance(tool, dict):
                issues.append(_issue("error", f"tools[{index}]", "Tool entry must be an object."))
                continue
            permissions = tool.get("permissions") or []
            permission_text = " ".join(str(item).lower() for item in permissions)
            if not permissions:
                issues.append(
                    _issue(
                        "warning",
                        f"tools[{index}].permissions",
                        "Permissions are empty.",
                    )
                )
            if tool.get("can_execute") and not any(
                term in permission_text for term in ("execute", "admin", "command")
            ):
                issues.append(
                    _issue(
                        "warning",
                        f"tools[{index}].permissions",
                        "can_execute=true but permissions do not mention execute/admin/command.",
                    )
                )
            if tool.get("can_write") and "write" not in permission_text:
                issues.append(
                    _issue(
                        "warning",
                        f"tools[{index}].permissions",
                        "can_write=true but permissions do not mention write.",
                    )
                )

    external_actions = payload.get("external_actions") or []
    if isinstance(external_actions, list):
        for index, action in enumerate(external_actions):
            if not isinstance(action, dict):
                issues.append(
                    _issue(
                        "error",
                        f"external_actions[{index}]",
                        "External action must be an object.",
                    )
                )
                continue
            if action.get("business_impact") not in ExternalActionSpec.allowed_business_impacts:
                issues.append(
                    _issue(
                        "error",
                        f"external_actions[{index}].business_impact",
                        "business_impact must be low, medium, or high.",
                    )
                )
            if action.get("business_impact") == "high" and action.get("reversible") is False:
                issues.append(
                    _issue(
                        "warning",
                        f"external_actions[{index}].reversible",
                        "High-impact action is not reversible.",
                    )
                )

    financial_tools = [
        tool
        for tool in tools
        if isinstance(tool, dict) and tool.get("can_trigger_financial_action") is True
    ]
    has_financial_action = any(
        isinstance(action, dict)
        and str(action.get("action_type", "")).lower()
        in {"transaction", "payment", "trade", "trading"}
        for action in external_actions
    )
    if financial_tools and not has_financial_action:
        issues.append(
            _issue(
                "error",
                "external_actions",
                "Financial-action tool exists but no transaction/payment/trade action is declared.",
            )
        )

    data_access = payload.get("data_access") or []
    has_sensitive_data = False
    if isinstance(data_access, list):
        for index, access in enumerate(data_access):
            if not isinstance(access, dict):
                issues.append(
                    _issue("error", f"data_access[{index}]", "Data access must be an object.")
                )
                continue
            sensitivity = access.get("sensitivity")
            if sensitivity not in DataAccessSpec.allowed_sensitivities:
                issues.append(
                    _issue(
                        "error",
                        f"data_access[{index}].sensitivity",
                        "sensitivity is not a supported value.",
                    )
                )
            if _is_sensitive(sensitivity):
                has_sensitive_data = True
                if access.get("pii_redaction") is False:
                    issues.append(
                        _issue(
                            "warning",
                            f"data_access[{index}].pii_redaction",
                            "Sensitive data exists but PII redaction is not declared.",
                        )
                    )

    logging = payload.get("logging") or {}
    if isinstance(logging, dict):
        retention_days = logging.get("retention_days")
        if retention_days is not None and retention_days < 0:
            issues.append(
                _issue("error", "logging.retention_days", "retention_days cannot be negative.")
            )
        if logging.get("input_output_logging") is True and has_sensitive_data:
            issues.append(
                _issue(
                    "warning",
                    "logging.input_output_logging",
                    (
                        "Input/output logging is enabled with sensitive data; document "
                        "redaction strategy."
                    ),
                )
            )

    memory = payload.get("memory") or {}
    if isinstance(memory, dict):
        if memory.get("uses_memory") is False and memory.get("contains_sensitive_data") is True:
            issues.append(
                _issue(
                    "error",
                    "memory.contains_sensitive_data",
                    "contains_sensitive_data cannot be true when uses_memory=false.",
                )
            )
        memory_type = memory.get("memory_type")
        if memory.get("uses_memory") is False and memory_type not in {None, "none"}:
            issues.append(
                _issue(
                    "error",
                    "memory.memory_type",
                    "memory_type must be none/null when uses_memory=false.",
                )
            )
        if memory.get("uses_memory") is True and memory_type in {None, "none"}:
            issues.append(
                _issue(
                    "error",
                    "memory.memory_type",
                    "memory_type must describe the active memory when uses_memory=true.",
                )
            )

    deployment = payload.get("deployment") or {}
    if isinstance(deployment, dict):
        if deployment.get("environment") not in DeploymentSpec.allowed_environments:
            issues.append(
                _issue(
                    "error",
                    "deployment.environment",
                    "deployment environment is not supported.",
                )
            )
        missing_customer_facing_controls = [
            field
            for field in ("incident_response_plan", "rollback_plan")
            if field not in deployment
        ]
        if deployment.get("environment") == "customer_facing" and missing_customer_facing_controls:
            issues.append(
                _issue(
                    "error",
                    "deployment",
                    (
                        "customer-facing workflow must declare incident response and "
                        "rollback plan fields."
                    ),
                )
            )
        if deployment.get("environment") == "customer_facing" and (
            deployment.get("incident_response_plan") is False
            or deployment.get("rollback_plan") is False
        ):
            issues.append(
                _issue(
                    "warning",
                    "deployment",
                    "customer-facing workflow has weak incident response or rollback controls.",
                )
            )

    evaluation = payload.get("evaluation") or {}
    if isinstance(evaluation, dict) and not any(bool(value) for value in evaluation.values()):
        issues.append(
            _issue("warning", "evaluation", "Workflow has no evaluation controls enabled.")
        )

    try:
        AgentWorkflow.model_validate(payload)
    except ValidationError as exc:
        for error in exc.errors():
            location = ".".join(str(part) for part in error.get("loc", ())) or "workflow"
            message = str(error.get("msg", "Validation failed."))
            issue = _issue("error", location, message)
            if issue not in issues:
                issues.append(issue)

    return issues


def validate_workflow_file(path: str | Path) -> list[ValidationIssue]:
    workflow_path = Path(path)
    try:
        payload = json.loads(workflow_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [_issue("error", str(workflow_path), f"Invalid JSON: {exc}")]
    if not isinstance(payload, dict):
        return [_issue("error", str(workflow_path), "Workflow file must contain a JSON object.")]
    return validate_workflow_payload(payload)
