# AgentGuard AI Assessment | Developer Code Agent

## Executive Summary
- Overall risk level: **High**
- Overall score: **0.67**
- Top risk drivers: tool_permission_risk, cybersecurity_risk, model_risk, operational_risk
- Most urgent control gaps: human_approval_gate, evaluation_suite, red_team_program, fallback_procedure, incident_response_plan

## Methodology
AgentGuard AI uses deterministic rules over a structured workflow description. It reviews tool permissions, data sensitivity, external actions, human oversight, logging, memory, evaluation controls, and deployment controls. No external LLM API, production system, or real customer data is used.

## Risk Scoring Explanation
| Component | Value |
|---|---|
| Max finding score | 0.79 |
| Mean top 5 score | 0.63 |
| Control gap density | 0.42 |
| Weighted score | 0.67 |
| Override applied | none |

## Workflow Overview
| Field | Value |
|---|---|
| Workflow ID | developer_code_agent |
| Business domain | software engineering |
| Agent type | coding_agent |
| Description | Assists developers by reading project files, editing source code, and executing local tests. |
| Tools | 3 |
| Data access categories | source_code (internal) |
| External actions | 1 |
| Human oversight | Enabled |
| Generated at | 2026-07-06T01:00:00 |

## Risk Findings
| Rule ID | Risk | Severity | Likelihood | Score | Framework Refs | Evidence Count | Affected Component | Recommended Controls |
|---|---|---|---|---|---|---|---|---|
| AG-RULE-TOOL-001 | tool_permission_risk | medium | medium | 0.50 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:file_writer | Restrict available tools to approved low-risk actions.; Require human approval before high-impact external actions. |
| AG-RULE-TOOL-001 | tool_permission_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:test_runner | Restrict available tools to approved low-risk actions.; Require human approval before high-impact external actions. |
| AG-RULE-CYBER-001 | cybersecurity_risk | high | medium | 0.69 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | tool:test_runner | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-MODEL-001 | model_risk | high | medium | 0.69 | NIST-AI-RMF-MEASURE | 4 | evaluation | Run task-specific quality, hallucination, and regression tests.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.; Define fallback behavior when the agent is uncertain or tools fail.; Require sources for factual claims. |
| AG-RULE-OPS-001 | operational_risk | medium | medium | 0.50 | NIST-AI-RMF-MANAGE | 4 | evaluation | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-OPS-001 | operational_risk | medium | medium | 0.50 | NIST-AI-RMF-MANAGE | 1 | deployment | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |

## Detailed Findings
### Tool permission is not approval-gated
- Rule ID: `AG-RULE-TOOL-001`
- Risk tag: `tool_permission_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: tool:file_writer
- Evidence:
  - Tool 'file_writer' has permissions: write.
  - requires_approval is false.
- Why it matters: The workflow gives the agent broad or potentially dangerous tool permissions without approval.
- Recommended controls:
  - Restrict available tools to approved low-risk actions.
  - Require human approval before high-impact external actions.
### Tool permission is not approval-gated
- Rule ID: `AG-RULE-TOOL-001`
- Risk tag: `tool_permission_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: tool:test_runner
- Evidence:
  - Tool 'test_runner' has permissions: execute.
  - requires_approval is false.
- Why it matters: The workflow gives the agent broad or potentially dangerous tool permissions without approval.
- Recommended controls:
  - Restrict available tools to approved low-risk actions.
  - Require human approval before high-impact external actions.
### Privileged tool execution risk
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: tool:test_runner
- Evidence:
  - Tool 'test_runner' exposes privileged permissions.
  - Declared permissions: execute_tests.
- Why it matters: The workflow exposes secrets, privileged tools, or sensitive data without enough security controls.
- Recommended controls:
  - Store API keys and credentials using safe secrets management.
  - Restrict available tools to approved low-risk actions.
  - Test agent behavior against direct and indirect prompt injection.
  - Define response process for agent failure, data leakage, or harmful action.
  - Review external providers for reliability, data handling, security posture, and operational dependency.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Protect system instructions and tool policies from disclosure or untrusted override.
  - Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.
### Model evaluation coverage is incomplete
- Rule ID: `AG-RULE-MODEL-001`
- Risk tag: `model_risk`
- Framework refs: NIST-AI-RMF-MEASURE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: evaluation
- Evidence:
  - Missing evaluation control: ongoing monitoring.
  - Missing evaluation control: red-team tests for agent/tool abuse.
  - Missing evaluation control: hallucination tests.
  - Missing evaluation control: fallback tests.
- Why it matters: The workflow has missing model quality, red-team, hallucination, monitoring, or fallback checks.
- Recommended controls:
  - Run task-specific quality, hallucination, and regression tests.
  - Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.
  - Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Require sources for factual claims.
### Operational monitoring or fallback is incomplete
- Rule ID: `AG-RULE-OPS-001`
- Risk tag: `operational_risk`
- Framework refs: NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: evaluation
- Evidence:
  - Missing evaluation control: ongoing monitoring.
  - Missing evaluation control: red-team tests for agent/tool abuse.
  - Missing evaluation control: hallucination tests.
  - Missing evaluation control: fallback tests.
- Why it matters: Missing fallback, monitoring, reversibility, rate-limit, rollback, or incident controls can delay recovery.
- Recommended controls:
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Define response process for agent failure, data leakage, or harmful action.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
  - Record all tool calls with timestamp, input, output, and outcome.
  - Limit frequency and volume of agent actions.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Operational resilience controls are incomplete
- Rule ID: `AG-RULE-OPS-001`
- Risk tag: `operational_risk`
- Framework refs: NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: deployment
- Evidence:
  - Missing deployment control: incident response plan.
- Why it matters: Missing fallback, monitoring, reversibility, rate-limit, rollback, or incident controls can delay recovery.
- Recommended controls:
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Define response process for agent failure, data leakage, or harmful action.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
  - Record all tool calls with timestamp, input, output, and outcome.
  - Limit frequency and volume of agent actions.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.

## Evidence Table
| Rule ID | Finding | Evidence |
|---|---|---|
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | Tool 'file_writer' has permissions: write. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | requires_approval is false. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | Tool 'test_runner' has permissions: execute. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | requires_approval is false. |
| AG-RULE-CYBER-001 | Privileged tool execution risk | Tool 'test_runner' exposes privileged permissions. |
| AG-RULE-CYBER-001 | Privileged tool execution risk | Declared permissions: execute_tests. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: ongoing monitoring. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: red-team tests for agent/tool abuse. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: hallucination tests. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: fallback tests. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: ongoing monitoring. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: red-team tests for agent/tool abuse. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: hallucination tests. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: fallback tests. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Missing deployment control: incident response plan. |

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
- `human_approval_gate`: Require human approval before high-impact external actions.
- `evaluation_suite`: Run task-specific quality, hallucination, and regression tests.
- `red_team_program`: Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.
- `fallback_procedure`: Define fallback behavior when the agent is uncertain or tools fail.
- `incident_response_plan`: Define response process for agent failure, data leakage, or harmful action.

### Existing Strengths
- Human-in-the-loop review is enabled.
- Tool-call logging is enabled.
- Audit export is available.
- Pre-deployment tests are defined.
- Secrets management is declared.

## Recommended Next Steps
- Split read, write, execute, and external-send permissions into separately approved tool scopes.
- Add a human approval gate before high-impact external actions such as outbound messages, API calls, file changes, or transactions.
- Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.
- Run structured red-team tests for prompt injection, data leakage, and tool misuse.
- Define fallback behavior for low-confidence outputs, tool failures, and missing evidence.
- Document an incident response process for data leakage, harmful tool use, and incorrect external actions.

## Assumptions and Limitations
- This assessment uses deterministic rules over the provided workflow JSON.
- It does not inspect live production systems, emails, brokers, CRM systems, or real customer records.
- It does not certify security, compliance, legal suitability, financial suitability, or investment suitability.
- Risk scores support portfolio demonstration and technical review; they are not regulatory ratings.

## Disclaimer
This assessment is a technical prototype for AI agent governance review. It is not legal, compliance, financial, investment, or security certification advice.