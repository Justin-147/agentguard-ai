"""Pydantic models for AI agent workflow risk assessments."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AgentGuardModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


def _lower(value: str) -> str:
    return value.strip().lower()


class ToolSpec(AgentGuardModel):
    name: str = Field(min_length=1)
    tool_type: str = Field(min_length=1)
    description: str = Field(min_length=1)
    permissions: list[str] = Field(default_factory=list)
    can_read: bool = False
    can_write: bool = False
    can_execute: bool = False
    can_send_external_message: bool = False
    can_trigger_financial_action: bool = False
    requires_approval: bool = False

    @model_validator(mode="after")
    def validate_financial_tool_type(self) -> ToolSpec:
        if self.can_trigger_financial_action and self.tool_type.lower() not in {
            "transaction",
            "payment",
            "trading",
            "api",
        }:
            raise ValueError(
                "Tools that can trigger financial actions must use "
                "transaction/payment/trading/api tool_type."
            )
        return self


class DataAccessSpec(AgentGuardModel):
    allowed_sensitivities: ClassVar[set[str]] = {
        "public",
        "internal",
        "confidential",
        "personal",
        "financial",
        "regulated",
    }

    data_category: str = Field(min_length=1)
    sensitivity: str
    purpose: str = Field(min_length=1)
    retention_policy_declared: bool
    pii_redaction: bool
    encryption_required: bool

    @field_validator("sensitivity")
    @classmethod
    def validate_sensitivity(cls, value: str) -> str:
        normalized = _lower(value)
        if normalized not in cls.allowed_sensitivities:
            raise ValueError(f"Unsupported data sensitivity: {value}")
        return normalized


class ExternalActionSpec(AgentGuardModel):
    allowed_business_impacts: ClassVar[set[str]] = {"low", "medium", "high"}

    action_type: str = Field(min_length=1)
    description: str = Field(min_length=1)
    requires_human_approval: bool
    reversible: bool
    business_impact: str

    @field_validator("business_impact")
    @classmethod
    def validate_business_impact(cls, value: str) -> str:
        normalized = _lower(value)
        if normalized not in cls.allowed_business_impacts:
            raise ValueError(f"Unsupported business impact: {value}")
        return normalized


class HumanOversightSpec(AgentGuardModel):
    allowed_review_frequencies: ClassVar[set[str]] = {
        "none",
        "sample",
        "daily",
        "weekly",
        "every_action",
    }

    human_in_the_loop: bool
    approval_required_for_high_risk_actions: bool
    review_frequency: str
    escalation_path_defined: bool

    @field_validator("review_frequency")
    @classmethod
    def validate_review_frequency(cls, value: str) -> str:
        normalized = _lower(value)
        if normalized not in cls.allowed_review_frequencies:
            raise ValueError(f"Unsupported review frequency: {value}")
        return normalized


class LoggingSpec(AgentGuardModel):
    tool_call_logging: bool
    input_output_logging: bool
    decision_trace: bool
    retention_days: int | None = Field(default=None, ge=0)
    audit_export_available: bool


class MemorySpec(AgentGuardModel):
    allowed_memory_types: ClassVar[set[str]] = {
        "none",
        "short_term",
        "long_term",
        "vector_store",
    }

    uses_memory: bool
    memory_type: str | None
    contains_sensitive_data: bool
    expiration_policy: bool
    user_deletion_supported: bool

    @field_validator("memory_type")
    @classmethod
    def validate_memory_type(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = _lower(value)
        if normalized not in cls.allowed_memory_types:
            raise ValueError(f"Unsupported memory type: {value}")
        return normalized

    @model_validator(mode="after")
    def validate_memory_consistency(self) -> MemorySpec:
        if not self.uses_memory and self.memory_type not in {None, "none"}:
            raise ValueError("memory_type must be 'none' or null when uses_memory is false.")
        if not self.uses_memory and self.contains_sensitive_data:
            raise ValueError("contains_sensitive_data cannot be true when uses_memory is false.")
        return self


class EvaluationSpec(AgentGuardModel):
    pre_deployment_tests: bool
    ongoing_monitoring: bool
    red_team_testing: bool
    hallucination_tests: bool
    prompt_injection_tests: bool
    fallback_tests: bool


class DeploymentSpec(AgentGuardModel):
    allowed_environments: ClassVar[set[str]] = {
        "local",
        "internal",
        "cloud",
        "customer_facing",
    }

    environment: str
    rate_limits: bool
    secrets_management: bool
    incident_response_plan: bool
    rollback_plan: bool

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        normalized = _lower(value)
        if normalized not in cls.allowed_environments:
            raise ValueError(f"Unsupported deployment environment: {value}")
        return normalized


class AgentWorkflow(AgentGuardModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    business_domain: str = Field(min_length=1)
    agent_type: str = Field(min_length=1)
    tools: list[ToolSpec]
    data_access: list[DataAccessSpec]
    external_actions: list[ExternalActionSpec]
    human_oversight: HumanOversightSpec
    logging: LoggingSpec
    memory: MemorySpec
    evaluation: EvaluationSpec
    deployment: DeploymentSpec

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", value):
            raise ValueError(
                "Workflow id may only contain letters, numbers, underscores, and hyphens."
            )
        return value

    @model_validator(mode="after")
    def validate_unique_tool_names(self) -> AgentWorkflow:
        names = [tool.name for tool in self.tools]
        if len(names) != len(set(names)):
            raise ValueError("Tool names must be unique.")
        return self


class RiskFinding(AgentGuardModel):
    allowed_severities: ClassVar[set[str]] = {"low", "medium", "high", "critical"}
    allowed_likelihoods: ClassVar[set[str]] = {"low", "medium", "high"}

    id: str
    rule_id: str
    risk_tag: str
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: str
    likelihood: str
    risk_score: float = Field(ge=0.0, le=1.0)
    affected_component: str = Field(min_length=1)
    evidence: list[str] = Field(default_factory=list)
    recommended_controls: list[str] = Field(default_factory=list)
    framework_refs: list[str] = Field(default_factory=list)

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: str) -> str:
        normalized = _lower(value)
        if normalized not in cls.allowed_severities:
            raise ValueError(f"Unsupported severity: {value}")
        return normalized

    @field_validator("likelihood")
    @classmethod
    def validate_likelihood(cls, value: str) -> str:
        normalized = _lower(value)
        if normalized not in cls.allowed_likelihoods:
            raise ValueError(f"Unsupported likelihood: {value}")
        return normalized


class AssessmentResult(AgentGuardModel):
    workflow_id: str
    workflow_name: str
    overall_risk_level: str
    overall_score: float = Field(ge=0.0, le=1.0)
    findings: list[RiskFinding]
    control_gaps: list[str]
    strengths: list[str]
    recommendations: list[str]
    score_explanation: dict[str, float | str] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
