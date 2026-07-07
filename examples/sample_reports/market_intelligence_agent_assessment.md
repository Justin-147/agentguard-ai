# AgentGuard AI Assessment | Market Intelligence Agent

## Executive Summary
- Overall risk level: **Medium**
- Overall score: **0.43**
- Top risk drivers: auditability_gap, model_risk
- Most urgent control gaps: evaluation_suite, red_team_program

## Methodology
AgentGuard AI uses deterministic rules over a structured workflow description. It reviews tool permissions, data sensitivity, external actions, human oversight, logging, memory, evaluation controls, and deployment controls. No external LLM API, production system, or real customer data is used.

## Risk Scoring Explanation
| Component | Value |
|---|---|
| Max finding score | 0.50 |
| Mean top 5 score | 0.50 |
| Control gap density | 0.17 |
| Weighted score | 0.43 |
| Override applied | none |

## Workflow Overview
| Field | Value |
|---|---|
| Workflow ID | market_intelligence_agent |
| Business domain | market research |
| Agent type | research_assistant |
| Description | Reads public web sources and generates internal market intelligence summaries with source links. |
| Tools | 2 |
| Data access categories | public_market_news (public) |
| External actions | 0 |
| Human oversight | Enabled |
| Generated at | 2026-07-06T01:00:00 |

## Risk Findings
| Rule ID | Risk | Severity | Likelihood | Score | Framework Refs | Evidence Count | Affected Component | Recommended Controls |
|---|---|---|---|---|---|---|---|---|
| AG-RULE-AUDIT-001 | auditability_gap | medium | medium | 0.50 | NIST-AI-RMF-GOVERN | 1 | logging | Record all tool calls with timestamp, input, output, and outcome.; Define and enforce data retention and deletion policy.; Require sources for factual claims.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Track data sources, transformations, outputs, and retention paths used by the agent workflow. |
| AG-RULE-MODEL-001 | model_risk | medium | medium | 0.50 | NIST-AI-RMF-MEASURE | 2 | evaluation | Run task-specific quality, hallucination, and regression tests.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.; Define fallback behavior when the agent is uncertain or tools fail.; Require sources for factual claims. |

## Detailed Findings
### Audit trail is incomplete
- Rule ID: `AG-RULE-AUDIT-001`
- Risk tag: `auditability_gap`
- Framework refs: NIST-AI-RMF-GOVERN
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: logging
- Evidence:
  - Missing audit feature: decision trace.
- Why it matters: The workflow may be difficult to investigate, replay, or evidence during governance review.
- Recommended controls:
  - Record all tool calls with timestamp, input, output, and outcome.
  - Define and enforce data retention and deletion policy.
  - Require sources for factual claims.
  - Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
### Model evaluation coverage is incomplete
- Rule ID: `AG-RULE-MODEL-001`
- Risk tag: `model_risk`
- Framework refs: NIST-AI-RMF-MEASURE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: evaluation
- Evidence:
  - Missing evaluation control: red-team tests for agent/tool abuse.
  - Missing evaluation control: hallucination tests.
- Why it matters: The workflow has missing model quality, red-team, hallucination, monitoring, or fallback checks.
- Recommended controls:
  - Run task-specific quality, hallucination, and regression tests.
  - Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.
  - Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Require sources for factual claims.

## Evidence Table
| Rule ID | Finding | Evidence |
|---|---|---|
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: decision trace. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: red-team tests for agent/tool abuse. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: hallucination tests. |

## Framework Mapping
| Framework Ref | Name | Mapped Risk Tags |
|---|---|---|
| OWASP-LLM01-2025 | Prompt Injection | prompt_injection_risk |
| OWASP-LLM02-2025 | Sensitive Information Disclosure | data_privacy_risk |
| OWASP-LLM06-2025 | Excessive Agency | tool_permission_risk, external_action_risk |
| NIST-AI-RMF-GOVERN | Govern | auditability_gap, human_oversight_gap |
| NIST-AI-RMF-MAP | Map | data_privacy_risk, third_party_risk |
| NIST-AI-RMF-MEASURE | Measure | model_risk |
| NIST-AI-RMF-MANAGE | Manage | operational_risk, cybersecurity_risk |

## Control Library
| Control | Description |
|---|---|
| human_approval_gate | Require human approval before high-impact external actions. |
| tool_allowlist | Restrict available tools to approved low-risk actions. |
| tool_call_audit_log | Record all tool calls with timestamp, input, output, and outcome. |
| pii_redaction | Redact or mask personal data before model processing. |
| retention_policy | Define and enforce data retention and deletion policy. |
| prompt_injection_tests | Test agent behavior against direct and indirect prompt injection. |
| evaluation_suite | Run task-specific quality, hallucination, and regression tests. |
| fallback_procedure | Define fallback behavior when the agent is uncertain or tools fail. |
| incident_response_plan | Define response process for agent failure, data leakage, or harmful action. |
| secrets_management | Store API keys and credentials using safe secrets management. |
| rate_limits | Limit frequency and volume of agent actions. |
| source_attribution | Require sources for factual claims. |
| regulated_records_control | Define controls for records that may be subject to regulated business processes. |
| vendor_due_diligence | Review external providers for reliability, data handling, security posture, and operational dependency. |
| third_party_contract_review | Document third-party responsibilities, data boundaries, incident handling, and service expectations. |
| model_card | Maintain a model or system card describing intended use, limitations, evaluation results, and known risks. |
| data_lineage | Track data sources, transformations, outputs, and retention paths used by the agent workflow. |
| embedding_store_access_control | Restrict and monitor access to vector stores or long-term memory containing sensitive content. |
| output_sanitization | Sanitize generated outputs before display, storage, or external transmission. |
| content_safety_filter | Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution. |
| system_prompt_protection | Protect system instructions and tool policies from disclosure or untrusted override. |
| budget_and_rate_guardrail | Set budget, volume, and rate guardrails for automated actions and external API usage. |
| human_escalation_path | Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| red_team_program | Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| privacy_impact_assessment | Assess privacy impact for personal, financial, confidential, or regulated data in the workflow. |

## Control Gap Summary
### Missing Controls
- `evaluation_suite`: Run task-specific quality, hallucination, and regression tests.
- `red_team_program`: Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.

### Existing Strengths
- Human-in-the-loop review is enabled.
- High-risk actions require approval.
- Tool-call logging is enabled.
- Audit export is available.
- Pre-deployment tests are defined.
- Ongoing monitoring is enabled.
- Secrets management is declared.
- Incident response planning is declared.
- No external actions are configured.

## Recommended Next Steps
- Make assessment replay possible by retaining tool-call logs, decision traces, and exportable audit records.
- Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.
- Run structured red-team tests for prompt injection, data leakage, and tool misuse.

## Assumptions and Limitations
- This assessment uses deterministic rules over the provided workflow JSON.
- It does not inspect live production systems, emails, brokers, CRM systems, or real customer records.
- It does not certify security, compliance, legal suitability, financial suitability, or investment suitability.
- Risk scores support portfolio demonstration and technical review; they are not regulatory ratings.

## Disclaimer
This assessment is a technical prototype for AI agent governance review. It is not legal, compliance, financial, investment, or security certification advice.