# AgentGuard AI Assessment | High Risk Autonomous Agent

## Executive Summary
- Overall risk level: **Critical**
- Overall score: **0.92**
- Top risk drivers: tool_permission_risk, external_action_risk, cybersecurity_risk, data_privacy_risk, auditability_gap
- Most urgent control gaps: retention_policy, pii_redaction, tool_call_audit_log, human_approval_gate, human_escalation_path

## Methodology
AgentGuard AI uses deterministic rules over a structured workflow description. It reviews tool permissions, data sensitivity, external actions, human oversight, logging, memory, evaluation controls, and deployment controls. No external LLM API, production system, or real customer data is used.

## Risk Scoring Explanation
| Component | Value |
|---|---|
| Max finding score | 0.93 |
| Mean top 5 score | 0.85 |
| Control gap density | 1.00 |
| Weighted score | 0.92 |
| Override applied | critical |

## Workflow Overview
| Field | Value |
|---|---|
| Workflow ID | high_risk_autonomous_agent |
| Business domain | financial services |
| Agent type | autonomous_agent |
| Description | A deliberately high-risk autonomous workflow that can message customers, call external APIs, trigger financial transactions, store sensitive memory, and act without approval. |
| Tools | 3 |
| Data access categories | customer_identity (personal), account_balances (financial), regulated_records (regulated) |
| External actions | 3 |
| Human oversight | Not enabled |
| Generated at | 2026-07-06T01:00:00 |

## Risk Findings
| Rule ID | Risk | Severity | Likelihood | Score | Framework Refs | Evidence Count | Affected Component | Recommended Controls |
|---|---|---|---|---|---|---|---|---|
| AG-RULE-ACTION-001 | external_action_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | external_action:email | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-HUMAN-001 | human_oversight_gap | high | medium | 0.69 | NIST-AI-RMF-GOVERN | 2 | external_action:email | Require human approval before high-impact external actions.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-OPS-001 | operational_risk | high | medium | 0.69 | NIST-AI-RMF-MANAGE | 2 | external_action:email | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-ACTION-001 | external_action_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | external_action:api_call | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-HUMAN-001 | human_oversight_gap | high | medium | 0.69 | NIST-AI-RMF-GOVERN | 2 | external_action:api_call | Require human approval before high-impact external actions.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-OPS-001 | operational_risk | high | medium | 0.69 | NIST-AI-RMF-MANAGE | 2 | external_action:api_call | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-ACTION-001 | external_action_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | external_action:transaction | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-HUMAN-001 | human_oversight_gap | high | medium | 0.69 | NIST-AI-RMF-GOVERN | 2 | external_action:transaction | Require human approval before high-impact external actions.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-OPS-001 | operational_risk | high | medium | 0.69 | NIST-AI-RMF-MANAGE | 2 | external_action:transaction | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-HUMAN-001 | human_oversight_gap | high | medium | 0.69 | NIST-AI-RMF-GOVERN | 2 | human_oversight | Require human approval before high-impact external actions.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-DATA-001 | data_privacy_risk | high | high | 0.79 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | data_access:customer_identity | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-CYBER-001 | cybersecurity_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | data_access:customer_identity | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-DATA-001 | data_privacy_risk | high | high | 0.79 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | data_access:account_balances | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-REG-001 | regulatory_risk | high | low | 0.60 | NIST-AI-RMF-GOVERN, NIST-AI-RMF-MAP | 2 | data_access:account_balances | Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Document third-party responsibilities, data boundaries, incident handling, and service expectations.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow. |
| AG-RULE-CYBER-001 | cybersecurity_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | data_access:account_balances | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-DATA-001 | data_privacy_risk | high | high | 0.79 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | data_access:regulated_records | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-REG-001 | regulatory_risk | high | medium | 0.69 | NIST-AI-RMF-GOVERN, NIST-AI-RMF-MAP | 2 | data_access:regulated_records | Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Document third-party responsibilities, data boundaries, incident handling, and service expectations.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow. |
| AG-RULE-CYBER-001 | cybersecurity_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | data_access:regulated_records | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-TOOL-001 | tool_permission_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:customer_email_sender | Restrict available tools to approved low-risk actions.; Require human approval before high-impact external actions. |
| AG-RULE-ACTION-001 | external_action_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:customer_email_sender | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-TOOL-001 | tool_permission_risk | high | high | 0.79 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:external_api_caller | Restrict available tools to approved low-risk actions.; Require human approval before high-impact external actions. |
| AG-RULE-CYBER-001 | cybersecurity_risk | high | medium | 0.69 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | tool:external_api_caller | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-TOOL-001 | tool_permission_risk | critical | high | 0.93 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:transaction_executor | Restrict available tools to approved low-risk actions.; Require human approval before high-impact external actions. |
| AG-RULE-ACTION-001 | external_action_risk | critical | high | 0.93 | OWASP-LLM06-2025, NIST-AI-RMF-MANAGE | 2 | tool:transaction_executor | Require human approval before high-impact external actions.; Limit frequency and volume of agent actions.; Set budget, volume, and rate guardrails for automated actions and external API usage. |
| AG-RULE-CYBER-001 | cybersecurity_risk | critical | medium | 0.82 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | tool:transaction_executor | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-AUDIT-001 | auditability_gap | high | high | 0.79 | NIST-AI-RMF-GOVERN | 5 | logging | Record all tool calls with timestamp, input, output, and outcome.; Define and enforce data retention and deletion policy.; Require sources for factual claims.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Track data sources, transformations, outputs, and retention paths used by the agent workflow. |
| AG-RULE-MODEL-001 | model_risk | high | medium | 0.69 | NIST-AI-RMF-MEASURE | 5 | evaluation | Run task-specific quality, hallucination, and regression tests.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.; Define fallback behavior when the agent is uncertain or tools fail.; Require sources for factual claims. |
| AG-RULE-OPS-001 | operational_risk | medium | medium | 0.50 | NIST-AI-RMF-MANAGE | 5 | evaluation | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-PROMPT-001 | prompt_injection_risk | high | medium | 0.69 | OWASP-LLM01-2025, NIST-AI-RMF-MEASURE | 2 | evaluation | Test agent behavior against direct and indirect prompt injection.; Protect system instructions and tool policies from disclosure or untrusted override.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-CYBER-001 | cybersecurity_risk | high | medium | 0.69 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | evaluation | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-OPS-001 | operational_risk | high | medium | 0.69 | NIST-AI-RMF-MANAGE | 3 | deployment | Define fallback behavior when the agent is uncertain or tools fail.; Define response process for agent failure, data leakage, or harmful action.; Set budget, volume, and rate guardrails for automated actions and external API usage.; Record all tool calls with timestamp, input, output, and outcome.; Limit frequency and volume of agent actions.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Define named escalation routes for uncertain, high-impact, or failed agent actions. |
| AG-RULE-CYBER-001 | cybersecurity_risk | high | medium | 0.69 | OWASP-LLM02-2025, NIST-AI-RMF-MANAGE | 2 | deployment | Store API keys and credentials using safe secrets management.; Restrict available tools to approved low-risk actions.; Test agent behavior against direct and indirect prompt injection.; Define response process for agent failure, data leakage, or harmful action.; Review external providers for reliability, data handling, security posture, and operational dependency.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission.; Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.; Protect system instructions and tool policies from disclosure or untrusted override.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs. |
| AG-RULE-MEMORY-001 | data_privacy_risk | high | high | 0.79 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 3 | memory | Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Define and enforce data retention and deletion policy.; Redact or mask personal data before model processing.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Sanitize generated outputs before display, storage, or external transmission.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow. |
| AG-RULE-THIRD-001 | third_party_risk | medium | medium | 0.50 | NIST-AI-RMF-MAP | 1 | tools | Review external providers for reliability, data handling, security posture, and operational dependency.; Document third-party responsibilities, data boundaries, incident handling, and service expectations.; Set budget, volume, and rate guardrails for automated actions and external API usage. |

## Detailed Findings
### External action lacks approval
- Rule ID: `AG-RULE-ACTION-001`
- Risk tag: `external_action_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: external_action:email
- Evidence:
  - Action 'email' has business impact 'high'.
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
- Severity / likelihood / score: high / medium / 0.69
- Affected component: external_action:email
- Evidence:
  - Action 'email' can run without human approval.
  - Workflow review frequency is 'none'.
- Why it matters: Medium or high impact agent actions should have explicit review, escalation, or approval before execution.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Operational resilience controls are incomplete
- Rule ID: `AG-RULE-OPS-001`
- Risk tag: `operational_risk`
- Framework refs: NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: external_action:email
- Evidence:
  - Action 'email' is high impact.
  - reversible is false.
- Why it matters: Missing fallback, monitoring, reversibility, rate-limit, rollback, or incident controls can delay recovery.
- Recommended controls:
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Define response process for agent failure, data leakage, or harmful action.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
  - Record all tool calls with timestamp, input, output, and outcome.
  - Limit frequency and volume of agent actions.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### External action lacks approval
- Rule ID: `AG-RULE-ACTION-001`
- Risk tag: `external_action_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: external_action:api_call
- Evidence:
  - Action 'api_call' has business impact 'high'.
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
- Severity / likelihood / score: high / medium / 0.69
- Affected component: external_action:api_call
- Evidence:
  - Action 'api_call' can run without human approval.
  - Workflow review frequency is 'none'.
- Why it matters: Medium or high impact agent actions should have explicit review, escalation, or approval before execution.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Operational resilience controls are incomplete
- Rule ID: `AG-RULE-OPS-001`
- Risk tag: `operational_risk`
- Framework refs: NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: external_action:api_call
- Evidence:
  - Action 'api_call' is high impact.
  - reversible is false.
- Why it matters: Missing fallback, monitoring, reversibility, rate-limit, rollback, or incident controls can delay recovery.
- Recommended controls:
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Define response process for agent failure, data leakage, or harmful action.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
  - Record all tool calls with timestamp, input, output, and outcome.
  - Limit frequency and volume of agent actions.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### External action lacks approval
- Rule ID: `AG-RULE-ACTION-001`
- Risk tag: `external_action_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: external_action:transaction
- Evidence:
  - Action 'transaction' has business impact 'high'.
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
- Severity / likelihood / score: high / medium / 0.69
- Affected component: external_action:transaction
- Evidence:
  - Action 'transaction' can run without human approval.
  - Workflow review frequency is 'none'.
- Why it matters: Medium or high impact agent actions should have explicit review, escalation, or approval before execution.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Operational resilience controls are incomplete
- Rule ID: `AG-RULE-OPS-001`
- Risk tag: `operational_risk`
- Framework refs: NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: external_action:transaction
- Evidence:
  - Action 'transaction' is high impact.
  - reversible is false.
- Why it matters: Missing fallback, monitoring, reversibility, rate-limit, rollback, or incident controls can delay recovery.
- Recommended controls:
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Define response process for agent failure, data leakage, or harmful action.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
  - Record all tool calls with timestamp, input, output, and outcome.
  - Limit frequency and volume of agent actions.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Approval gap for external action
- Rule ID: `AG-RULE-HUMAN-001`
- Risk tag: `human_oversight_gap`
- Framework refs: NIST-AI-RMF-GOVERN
- Severity / likelihood / score: high / medium / 0.69
- Affected component: human_oversight
- Evidence:
  - At least one external action has high business impact.
  - escalation_path_defined is false.
- Why it matters: Medium or high impact agent actions should have explicit review, escalation, or approval before execution.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Sensitive data controls are incomplete
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: high / high / 0.79
- Affected component: data_access:customer_identity
- Evidence:
  - Data category 'customer_identity' is marked 'personal'.
  - Missing: retention policy, PII redaction.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Sensitive data encryption is not required
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: data_access:customer_identity
- Evidence:
  - Data category 'customer_identity' is 'personal'.
  - encryption_required is false.
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
### Sensitive data controls are incomplete
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: high / high / 0.79
- Affected component: data_access:account_balances
- Evidence:
  - Data category 'account_balances' is marked 'financial'.
  - Missing: retention policy, PII redaction.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Regulated or financial data exposure
- Rule ID: `AG-RULE-REG-001`
- Risk tag: `regulatory_risk`
- Framework refs: NIST-AI-RMF-GOVERN, NIST-AI-RMF-MAP
- Severity / likelihood / score: high / low / 0.60
- Affected component: data_access:account_balances
- Evidence:
  - Data sensitivity is 'financial'.
  - Privacy controls missing: retention policy, PII redaction.
- Why it matters: Financial or regulated data increases the need for controlled records, monitoring, and review.
- Recommended controls:
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Document third-party responsibilities, data boundaries, incident handling, and service expectations.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
### Sensitive data encryption is not required
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: data_access:account_balances
- Evidence:
  - Data category 'account_balances' is 'financial'.
  - encryption_required is false.
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
### Sensitive data controls are incomplete
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: high / high / 0.79
- Affected component: data_access:regulated_records
- Evidence:
  - Data category 'regulated_records' is marked 'regulated'.
  - Missing: retention policy, PII redaction.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Regulated or financial data exposure
- Rule ID: `AG-RULE-REG-001`
- Risk tag: `regulatory_risk`
- Framework refs: NIST-AI-RMF-GOVERN, NIST-AI-RMF-MAP
- Severity / likelihood / score: high / medium / 0.69
- Affected component: data_access:regulated_records
- Evidence:
  - Data sensitivity is 'regulated'.
  - Privacy controls missing: retention policy, PII redaction.
- Why it matters: Financial or regulated data increases the need for controlled records, monitoring, and review.
- Recommended controls:
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Document third-party responsibilities, data boundaries, incident handling, and service expectations.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
### Sensitive data encryption is not required
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: data_access:regulated_records
- Evidence:
  - Data category 'regulated_records' is 'regulated'.
  - encryption_required is false.
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
### Tool permission is not approval-gated
- Rule ID: `AG-RULE-TOOL-001`
- Risk tag: `tool_permission_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: tool:customer_email_sender
- Evidence:
  - Tool 'customer_email_sender' has permissions: send_external_message.
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
- Affected component: tool:customer_email_sender
- Evidence:
  - Tool 'customer_email_sender' can send external messages or trigger financial action.
  - requires_approval is false.
- Why it matters: The agent can take an outward-facing or business-impacting action without a human approval gate.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Limit frequency and volume of agent actions.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
### Tool permission is not approval-gated
- Rule ID: `AG-RULE-TOOL-001`
- Risk tag: `tool_permission_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / high / 0.79
- Affected component: tool:external_api_caller
- Evidence:
  - Tool 'external_api_caller' has permissions: execute.
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
- Affected component: tool:external_api_caller
- Evidence:
  - Tool 'external_api_caller' exposes privileged permissions.
  - Declared permissions: call_external_api, read_customer_data.
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
### Tool permission is not approval-gated
- Rule ID: `AG-RULE-TOOL-001`
- Risk tag: `tool_permission_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: critical / high / 0.93
- Affected component: tool:transaction_executor
- Evidence:
  - Tool 'transaction_executor' has permissions: write, execute, trigger_financial_action.
  - requires_approval is false.
- Why it matters: The workflow gives the agent broad or potentially dangerous tool permissions without approval.
- Recommended controls:
  - Restrict available tools to approved low-risk actions.
  - Require human approval before high-impact external actions.
### Tool can trigger external impact
- Rule ID: `AG-RULE-ACTION-001`
- Risk tag: `external_action_risk`
- Framework refs: OWASP-LLM06-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: critical / high / 0.93
- Affected component: tool:transaction_executor
- Evidence:
  - Tool 'transaction_executor' can send external messages or trigger financial action.
  - requires_approval is false.
- Why it matters: The agent can take an outward-facing or business-impacting action without a human approval gate.
- Recommended controls:
  - Require human approval before high-impact external actions.
  - Limit frequency and volume of agent actions.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
### Privileged tool execution risk
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: critical / medium / 0.82
- Affected component: tool:transaction_executor
- Evidence:
  - Tool 'transaction_executor' exposes privileged permissions.
  - Declared permissions: execute_transaction, admin_transaction.
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
### Audit trail is incomplete
- Rule ID: `AG-RULE-AUDIT-001`
- Risk tag: `auditability_gap`
- Framework refs: NIST-AI-RMF-GOVERN
- Severity / likelihood / score: high / high / 0.79
- Affected component: logging
- Evidence:
  - Missing audit feature: tool-call logging.
  - Missing audit feature: input/output logging for sensitive-data workflow.
  - Missing audit feature: decision trace.
  - Missing audit feature: audit export.
  - Missing audit feature: log retention period.
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
  - Missing evaluation control: pre-deployment tests.
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
  - Missing evaluation control: pre-deployment tests.
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
### Untrusted content lacks prompt-injection testing
- Rule ID: `AG-RULE-PROMPT-001`
- Risk tag: `prompt_injection_risk`
- Framework refs: OWASP-LLM01-2025, NIST-AI-RMF-MEASURE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: evaluation
- Evidence:
  - Untrusted input sources detected: email, external_api.
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
  - Untrusted input sources detected: email, external_api.
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
### Operational resilience controls are incomplete
- Rule ID: `AG-RULE-OPS-001`
- Risk tag: `operational_risk`
- Framework refs: NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: deployment
- Evidence:
  - Missing deployment control: incident response plan.
  - Missing deployment control: rollback plan.
  - Missing deployment control: rate limits.
- Why it matters: Missing fallback, monitoring, reversibility, rate-limit, rollback, or incident controls can delay recovery.
- Recommended controls:
  - Define fallback behavior when the agent is uncertain or tools fail.
  - Define response process for agent failure, data leakage, or harmful action.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.
  - Record all tool calls with timestamp, input, output, and outcome.
  - Limit frequency and volume of agent actions.
  - Filter unsafe, malicious, or policy-violating inputs and outputs before tool execution.
  - Define named escalation routes for uncertain, high-impact, or failed agent actions.
### Secrets management is missing for privileged tools
- Rule ID: `AG-RULE-CYBER-001`
- Risk tag: `cybersecurity_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MANAGE
- Severity / likelihood / score: high / medium / 0.69
- Affected component: deployment
- Evidence:
  - secrets_management is false.
  - Workflow includes API, execution, external-send, or transaction-capable tools.
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
### Sensitive memory controls are incomplete
- Rule ID: `AG-RULE-MEMORY-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: high / high / 0.79
- Affected component: memory
- Evidence:
  - memory_type is 'long_term'.
  - Missing memory control: memory expiration policy.
  - Missing memory control: user deletion support.
- Why it matters: Long-lived or vector memory that contains sensitive data should support access controls, expiration, and deletion.
- Recommended controls:
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Define and enforce data retention and deletion policy.
  - Redact or mask personal data before model processing.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Sanitize generated outputs before display, storage, or external transmission.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
### External API dependency is present
- Rule ID: `AG-RULE-THIRD-001`
- Risk tag: `third_party_risk`
- Framework refs: NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: tools
- Evidence:
  - Workflow includes an API tool or API-call external action.
- Why it matters: External providers and APIs introduce availability, data handling, and vendor-control considerations.
- Recommended controls:
  - Review external providers for reliability, data handling, security posture, and operational dependency.
  - Document third-party responsibilities, data boundaries, incident handling, and service expectations.
  - Set budget, volume, and rate guardrails for automated actions and external API usage.

## Evidence Table
| Rule ID | Finding | Evidence |
|---|---|---|
| AG-RULE-ACTION-001 | External action lacks approval | Action 'email' has business impact 'high'. |
| AG-RULE-ACTION-001 | External action lacks approval | requires_human_approval is false. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Action 'email' can run without human approval. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Workflow review frequency is 'none'. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Action 'email' is high impact. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | reversible is false. |
| AG-RULE-ACTION-001 | External action lacks approval | Action 'api_call' has business impact 'high'. |
| AG-RULE-ACTION-001 | External action lacks approval | requires_human_approval is false. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Action 'api_call' can run without human approval. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Workflow review frequency is 'none'. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Action 'api_call' is high impact. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | reversible is false. |
| AG-RULE-ACTION-001 | External action lacks approval | Action 'transaction' has business impact 'high'. |
| AG-RULE-ACTION-001 | External action lacks approval | requires_human_approval is false. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Action 'transaction' can run without human approval. |
| AG-RULE-HUMAN-001 | Approval gap for external action | Workflow review frequency is 'none'. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Action 'transaction' is high impact. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | reversible is false. |
| AG-RULE-HUMAN-001 | Approval gap for external action | At least one external action has high business impact. |
| AG-RULE-HUMAN-001 | Approval gap for external action | escalation_path_defined is false. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Data category 'customer_identity' is marked 'personal'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Missing: retention policy, PII redaction. |
| AG-RULE-CYBER-001 | Sensitive data encryption is not required | Data category 'customer_identity' is 'personal'. |
| AG-RULE-CYBER-001 | Sensitive data encryption is not required | encryption_required is false. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Data category 'account_balances' is marked 'financial'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Missing: retention policy, PII redaction. |
| AG-RULE-REG-001 | Regulated or financial data exposure | Data sensitivity is 'financial'. |
| AG-RULE-REG-001 | Regulated or financial data exposure | Privacy controls missing: retention policy, PII redaction. |
| AG-RULE-CYBER-001 | Sensitive data encryption is not required | Data category 'account_balances' is 'financial'. |
| AG-RULE-CYBER-001 | Sensitive data encryption is not required | encryption_required is false. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Data category 'regulated_records' is marked 'regulated'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Missing: retention policy, PII redaction. |
| AG-RULE-REG-001 | Regulated or financial data exposure | Data sensitivity is 'regulated'. |
| AG-RULE-REG-001 | Regulated or financial data exposure | Privacy controls missing: retention policy, PII redaction. |
| AG-RULE-CYBER-001 | Sensitive data encryption is not required | Data category 'regulated_records' is 'regulated'. |
| AG-RULE-CYBER-001 | Sensitive data encryption is not required | encryption_required is false. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | Tool 'customer_email_sender' has permissions: send_external_message. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | requires_approval is false. |
| AG-RULE-ACTION-001 | Tool can trigger external impact | Tool 'customer_email_sender' can send external messages or trigger financial action. |
| AG-RULE-ACTION-001 | Tool can trigger external impact | requires_approval is false. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | Tool 'external_api_caller' has permissions: execute. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | requires_approval is false. |
| AG-RULE-CYBER-001 | Privileged tool execution risk | Tool 'external_api_caller' exposes privileged permissions. |
| AG-RULE-CYBER-001 | Privileged tool execution risk | Declared permissions: call_external_api, read_customer_data. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | Tool 'transaction_executor' has permissions: write, execute, trigger_financial_action. |
| AG-RULE-TOOL-001 | Tool permission is not approval-gated | requires_approval is false. |
| AG-RULE-ACTION-001 | Tool can trigger external impact | Tool 'transaction_executor' can send external messages or trigger financial action. |
| AG-RULE-ACTION-001 | Tool can trigger external impact | requires_approval is false. |
| AG-RULE-CYBER-001 | Privileged tool execution risk | Tool 'transaction_executor' exposes privileged permissions. |
| AG-RULE-CYBER-001 | Privileged tool execution risk | Declared permissions: execute_transaction, admin_transaction. |
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: tool-call logging. |
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: input/output logging for sensitive-data workflow. |
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: decision trace. |
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: audit export. |
| AG-RULE-AUDIT-001 | Audit trail is incomplete | Missing audit feature: log retention period. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: pre-deployment tests. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: ongoing monitoring. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: red-team tests for agent/tool abuse. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: hallucination tests. |
| AG-RULE-MODEL-001 | Model evaluation coverage is incomplete | Missing evaluation control: fallback tests. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: pre-deployment tests. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: ongoing monitoring. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: red-team tests for agent/tool abuse. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: hallucination tests. |
| AG-RULE-OPS-001 | Operational monitoring or fallback is incomplete | Missing evaluation control: fallback tests. |
| AG-RULE-PROMPT-001 | Untrusted content lacks prompt-injection testing | Untrusted input sources detected: email, external_api. |
| AG-RULE-PROMPT-001 | Untrusted content lacks prompt-injection testing | prompt_injection_tests is false. |
| AG-RULE-CYBER-001 | Prompt injection can affect tool use | Untrusted input sources detected: email, external_api. |
| AG-RULE-CYBER-001 | Prompt injection can affect tool use | Prompt-injection testing is not declared. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Missing deployment control: incident response plan. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Missing deployment control: rollback plan. |
| AG-RULE-OPS-001 | Operational resilience controls are incomplete | Missing deployment control: rate limits. |
| AG-RULE-CYBER-001 | Secrets management is missing for privileged tools | secrets_management is false. |
| AG-RULE-CYBER-001 | Secrets management is missing for privileged tools | Workflow includes API, execution, external-send, or transaction-capable tools. |
| AG-RULE-MEMORY-001 | Sensitive memory controls are incomplete | memory_type is 'long_term'. |
| AG-RULE-MEMORY-001 | Sensitive memory controls are incomplete | Missing memory control: memory expiration policy. |
| AG-RULE-MEMORY-001 | Sensitive memory controls are incomplete | Missing memory control: user deletion support. |
| AG-RULE-THIRD-001 | External API dependency is present | Workflow includes an API tool or API-call external action. |

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
- `retention_policy`: Define and enforce data retention and deletion policy.
- `pii_redaction`: Redact or mask personal data before model processing.
- `tool_call_audit_log`: Record all tool calls with timestamp, input, output, and outcome.
- `human_approval_gate`: Require human approval before high-impact external actions.
- `human_escalation_path`: Define named escalation routes for uncertain, high-impact, or failed agent actions.
- `prompt_injection_tests`: Test agent behavior against direct and indirect prompt injection.
- `evaluation_suite`: Run task-specific quality, hallucination, and regression tests.
- `red_team_program`: Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.
- `fallback_procedure`: Define fallback behavior when the agent is uncertain or tools fail.
- `incident_response_plan`: Define response process for agent failure, data leakage, or harmful action.
- `secrets_management`: Store API keys and credentials using safe secrets management.
- `rate_limits`: Limit frequency and volume of agent actions.
- `regulated_records_control`: Define controls for records that may be subject to regulated business processes.
- `vendor_due_diligence`: Review external providers for reliability, data handling, security posture, and operational dependency.

### Existing Strengths
- No explicit strengths were identified.

## Recommended Next Steps
- Review the 'external_action:email' action path and require approval when business impact is medium or high.
- Review the 'external_action:api_call' action path and require approval when business impact is medium or high.
- Review the 'external_action:transaction' action path and require approval when business impact is medium or high.
- Classify sensitive input fields, redact personal data where possible, and document retention for each data category.
- Split read, write, execute, and external-send permissions into separately approved tool scopes.
- Review the 'tool:customer_email_sender' action path and require approval when business impact is medium or high.
- Review the 'tool:transaction_executor' action path and require approval when business impact is medium or high.
- Make assessment replay possible by retaining tool-call logs, decision traces, and exportable audit records.
- Define and enforce a retention policy for inputs, outputs, logs, and memory records.
- Redact or mask personal and financial identifiers before model processing or long-term storage.
- Enable tool-call audit logging with timestamp, tool name, input summary, output summary, and execution status.
- Add a human approval gate before high-impact external actions such as outbound messages, API calls, file changes, or transactions.
- Define a named escalation path for uncertain, failed, or high-impact agent actions.
- Add direct and indirect prompt-injection tests for untrusted emails, web pages, uploaded documents, and customer messages.
- Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.
- Run structured red-team tests for prompt injection, data leakage, and tool misuse.
- Define fallback behavior for low-confidence outputs, tool failures, and missing evidence.
- Document an incident response process for data leakage, harmful tool use, and incorrect external actions.
- Store API keys and credentials in a secrets manager or environment-managed secret store.
- Apply rate limits to constrain the frequency and volume of automated agent actions.
- Define recordkeeping controls for regulated or financial workflow records.
- Review external API and vendor dependencies for reliability, data handling, and security posture.
- Require source attribution for financial summaries and portfolio-related factual claims.

## Assumptions and Limitations
- This assessment uses deterministic rules over the provided workflow JSON.
- It does not inspect live production systems, emails, brokers, CRM systems, or real customer records.
- It does not certify security, compliance, legal suitability, financial suitability, or investment suitability.
- Risk scores support portfolio demonstration and technical review; they are not regulatory ratings.

## Disclaimer
This assessment is a technical prototype for AI agent governance review. It is not legal, compliance, financial, investment, or security certification advice.