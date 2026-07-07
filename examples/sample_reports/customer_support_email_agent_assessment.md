# AgentGuard AI Assessment | Customer Support Email Agent

## Executive Summary
- Overall risk level: **High**
- Overall score: **0.71**
- Top risk drivers: tool_permission_risk, external_action_risk, model_risk, prompt_injection_risk, cybersecurity_risk
- Most urgent control gaps: pii_redaction, output_sanitization, human_approval_gate, prompt_injection_tests, evaluation_suite

## Methodology
AgentGuard AI uses deterministic rules over a structured workflow description. It reviews tool permissions, data sensitivity, external actions, human oversight, logging, memory, evaluation controls, and deployment controls. No external LLM API, production system, or real customer data is used.

## Risk Scoring Explanation
| Component | Value |
|---|---|
| Max finding score | 0.79 |
| Mean top 5 score | 0.73 |
| Control gap density | 0.50 |
| Weighted score | 0.71 |
| Override applied | none |

## Workflow Overview
| Field | Value |
|---|---|
| Workflow ID | customer_support_email_agent |
| Business domain | customer support |
| Agent type | email_agent |
| Description | Reads customer support tickets, drafts responses, and can send approved-looking outbound emails to customers. |
| Tools | 2 |
| Data access categories | customer_messages (personal) |
| External actions | 1 |
| Human oversight | Enabled |
| Generated at | 2026-07-06T01:00:00 |

## Risk Findings
| Rule ID | Risk | Severity | Likelihood | Score | Framework Refs | Evidence Count | Affected Component | Recommended Controls |
|---|---|---|---|---|---|---|---|---|
| AG-RULE-ACTION-001 | external_action_risk | medium | high | 0.60 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | external_action:email | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-HUMAN-001 | human_oversight_gap | medium | medium | 0.50 | NIST-AI-RMF-GOVERN | 2 | external_action:email | Require human approval before high-impact external actions.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-DATA-001 | data_privacy_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | data_access:customer_messages | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-DATA-001 | data_privacy_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | logging:customer_messages | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-TOOL-001 | tool_permission_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:email_sender | Restrict available tools to approved low-risk actions.; Require human approval before high-impact external actions. |
| AG-RULE-ACTION-001 | external_action_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:email_sender | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-AUDIT-001 | auditability_gap | medium | medium | 0.50 | NIST-AI-RMF-GOVERN | 1 | logging | Record all tool calls with timestamp, input, output, and outcome.; Define and enforce data retention and deletion policy.; Require sources for factual claims.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Track data sources, transformations, outputs, and retention paths used by the agent workflow. |
| AG-RULE-MODEL-001 | model_risk | high | medium | 0.69 | NIST-AI-RMF-MEASURE | 2 | evaluation | Run task-specific quality, hallucination, and regression tests.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.; Define fallback behavior when the agent is uncertain or tools fail.; Require sources for factual claims. |
| AG-RULE-PROMPT-001 | prompt_injection_risk | high | medium | 0.69 | OWASP-LLM01-2025, NIST-AI-RMF-MEASURE | 2 | evaluation | Test agent behavior against direct and indirect prompt injection.; Protect system instructions and tool policies from disclosure or untrusted override.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-CYBER-001 | cybersecurity_risk | high | medium | 0.69 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | evaluation | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |

## Detailed Findings
### External action lacks approval
- Rule ID: `AG-RULE-ACTION-001`
- Risk tag: `external_action_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / high / 0.60
- Affected component: external_action:email
- Evidence:
  - Action 'email' has business impact 'medium'.
  - requires_human_approval is false.
- Why it matters: The agent can take an outward-facing or business-impacting action without a human approval gate.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Limit frequency and volume of agent actions.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
### Approval gap for external action
- Rule ID: `AG-RULE-HUMAN-001`
- Risk tag: `human_oversight_gap`
- Framework refs: NIST-AI-RMF-GOVERN
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: external_action:email
- Evidence:
  - Action 'email' can run without human approval.
  - Workflow review frequency is 'sample'.
- Why it matters: Medium or high impact agent actions should have explicit review, escalation, or approval before execution.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Sensitive data controls are incomplete
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: data_access:customer_messages
- Evidence:
  - Data category 'customer_messages' is marked 'personal'.
  - Missing: PII redaction.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Input/output logs may capture unredacted sensitive data
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: logging:customer_messages
- Evidence:
  - input_output_logging is true for a workflow with sensitive data.
  - Data category 'customer_messages' has pii_redaction=false.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Tool permission is not approval-gated
- Rule ID: `AG-RULE-TOOL-001`
- Risk tag: `tool_permission_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: tool:email_sender
- Evidence:
  - Tool 'email_sender' has permissions: send_external_message.
  - requires_approval is false.
- Why it matters: The workflow gives the agent broad or potentially dangerous tool permissions without approval.
- Recommended controls:
  - Restrict available tools to approved low-risk actions.
  - Require human approval before high-impact external actions.
### Tool can trigger external impact
- Rule ID: `AG-RULE-ACTION-001`
- Risk tag: `external_action_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: tool:email_sender
- Evidence:
  - Tool 'email_sender' can send external messages or trigger financial action.
  - requires_approval is false.
- Why it matters: The agent can take an outward-facing or business-impacting action without a human approval gate.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Limit frequency and volume of agent actions.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
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
- Severity / likelihood / score: high / medium / 0.69
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
### Untrusted content lacks prompt-injection testing
- Rule ID: `AG-RULE-PROMPT-001`
- Risk tag: `prompt_injection_risk`
- Framework refs: OWASP-LLM01-2025, NIST-AI-RMF-MEASURE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: evaluation
- Evidence:
  - Untrusted input sources detected: email, ticket.
  - prompt_injection_tests is false.
- Why it matters: Agents that read emails, web content, uploaded documents, customer messages, or external APIs need prompt-injection controls.
- Recommended controls:
  - Test agent behavior against direct and indirect prompt injection.
  - Protect system instructions and tool policies from disclosure or untrusted override.
  - Sanitize generated outputs before display, storage, or external transmission.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.
### Prompt injection can affect tool use
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: evaluation
- Evidence:
  - Untrusted input sources detected: email, ticket.
  - Prompt-injection testing is not declared.
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

## Evidence Table
| Rule ID | Finding | Evidence |
|---|---|---|
| AG-RULE-ACTION-001 | External action lacks approval | Action 'email' has business impact 'medium'. |
| AG-RULE-ACTION-001 | External action lacks approval | requires_human_approval is false. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Action 'email' can run without human approval. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Workflow review frequency is 'sample'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Data category 'customer_messages' is marked 'personal'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Missing: PII redaction. |
| AG-RULE-DATA-001 | Input/output logs may capture unredacted sensitive data | input_output_logging is true for a workflow with sensitive data. |
| AG-RULE-DATA-001 | Input/output logs may capture unredacted sensitive data | Data category 'customer_messages' has pii_redaction=false. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | Tool 'email_sender' has permissions: send_external_message. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | requires_approval is false. |
| AG-RULE-ACTION-001 | Tool can trigger external impact | Tool 'email_sender' can send external messages or trigger financial action. |
| AG-RULE-ACTION-001 | Tool can trigger external impact | requires_approval is false. |
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: decision trace. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: red-team tests for agent/tool abuse. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: hallucination tests. |
| AG-RULE-PROMPT-001 | Untrusted content lacks prompt-injection testing | Untrusted input sources detected: email, ticket. |
| AG-RULE-PROMPT-001 | Untrusted content lacks prompt-injection testing | prompt_injection_tests is false. |
| AG-RULE-CYBER-001 | Prompt injection can affect tool use | Untrusted input sources detected: email, ticket. |
| AG-RULE-CYBER-001 | Prompt injection can affect tool use | Prompt-injection testing is not declared. |

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
- `pii_redaction`: Redact or mask personal data before model processing.
- `output_sanitization`: Sanitize generated outputs before display, storage, or external transmission.
- `human_approval_gate`: Require human approval before high-impact external actions.
- `prompt_injection_tests`: Test agent behavior against direct and indirect prompt injection.
- `evaluation_suite`: Run task-specific quality, hallucination, and regression tests.
- `red_team_program`: Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.

### Existing Strengths
- Human-in-the-loop review is enabled.
- Tool-call logging is enabled.
- Audit export is available.
- Pre-deployment tests are defined.
- Ongoing monitoring is enabled.
- Secrets management is declared.
- Incident response planning is declared.

## Recommended Next Steps
- Review the 'external_action:email' action path and require approval when business impact is medium or high.
- Classify sensitive input fields, redact personal data where possible, and document retention for each data category.
- Split read, write, execute, and external-send permissions into separately approved tool scopes.
- Review the 'tool:email_sender' action path and require approval when business impact is medium or high.
- Make assessment replay possible by retaining tool-call logs, decision traces, and exportable audit records.
- Redact or mask personal and financial identifiers before model processing or long-term storage.
- Sanitize generated outputs before storage, display, or external transmission.
- Add a human approval gate before high-impact external actions such as outbound messages, API calls, file changes, or transactions.
- Add direct and indirect prompt-injection tests for untrusted emails, web pages, uploaded documents, and customer messages.
- Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.
- Run structured red-team tests for prompt injection, data leakage, and tool misuse.

## Assumptions and Limitations
- This assessment uses deterministic rules over the provided workflow JSON.
- It does not inspect live production systems, emails, brokers, CRM systems, or real customer records.
- It does not certify security, compliance, legal suitability, financial suitability, or investment suitability.
- Risk scores support portfolio demonstration and technical review; they are not regulatory ratings.

## Disclaimer
This assessment is a technical prototype for AI agent governance review. It is not legal, compliance, financial, investment, or security certification advice.