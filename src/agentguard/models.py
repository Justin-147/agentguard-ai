"""Pydantic models for AI agent workflow risk assessments."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentGuardModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


def _lower(value: str) -> str:
    return value.strip().lower()


class ToolSpec(AgentGuardModel):
    name: str
    tool_type: str
    description: str
    permissions: list[str]
    can_read: bool = False
    can_write: bool = False
    can_execute: bool = False
    can_send_external_message: bool = False
    can_trigger_financial_action: bool = False
    requires_approval: bool = False


class DataAccessSpec(AgentGuardModel):
    allowed_sensitivities: ClassVar[set[str]] = {
        "public",
        "internal",
        "confidential",
        "personal",
        "financial",
        "regulated",
    }

    data_category: str
    sensitivity: str
    purpose: str
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

    action_type: str
    description: str
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
    retention_days: int | None
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
    id: str
    name: str
    description: str
    business_domain: str
    agent_type: str
    tools: list[ToolSpec]
    data_access: list[DataAccessSpec]
    external_actions: list[ExternalActionSpec]
    human_oversight: HumanOversightSpec
    logging: LoggingSpec
    memory: MemorySpec
    evaluation: EvaluationSpec
    deployment: DeploymentSpec


class RiskFinding(AgentGuardModel):
    allowed_severities: ClassVar[set[str]] = {"low", "medium", "high", "critical"}
    allowed_likelihoods: ClassVar[set[str]] = {"low", "medium", "high"}

    id: str
    risk_tag: str
    title: str
    description: str
    severity: str
    likelihood: str
    risk_score: float = Field(ge=0.0, le=1.0)
    affected_component: str
    evidence: list[str]
    recommended_controls: list[str]

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
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
