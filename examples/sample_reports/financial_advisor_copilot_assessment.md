# AgentGuard AI Assessment | Financial Advisor Copilot

## Executive Summary
- Overall risk level: **Medium**
- Overall score: **0.54**
- Top risk drivers: data_privacy_risk, regulatory_risk, model_risk
- Most urgent control gaps: retention_policy, pii_redaction, output_sanitization, evaluation_suite, red_team_program

## Methodology
AgentGuard AI uses deterministic rules over a structured workflow description. It reviews tool permissions, data sensitivity, external actions, human oversight, logging, memory, evaluation controls, and deployment controls. No external LLM API, production system, or real customer data is used.

## Risk Scoring Explanation
| Component | Value |
|---|---|
| Max finding score | 0.60 |
| Mean top 5 score | 0.52 |
| Control gap density | 0.42 |
| Weighted score | 0.54 |
| Override applied | none |

## Workflow Overview
| Field | Value |
|---|---|
| Workflow ID | financial_advisor_copilot |
| Business domain | wealth management |
| Agent type | advisor_copilot |
| Description | Assists relationship managers by summarizing customer profiles and portfolio notes. It cannot place trades or send external messages. |
| Tools | 2 |
| Data access categories | customer_profile (personal), portfolio_notes (financial) |
| External actions | 0 |
| Human oversight | Enabled |
| Generated at | 2026-07-06T01:00:00 |

## Risk Findings
| Rule ID | Risk | Severity | Likelihood | Score | Framework Refs | Evidence Count | Affected Component | Recommended Controls |
|---|---|---|---|---|---|---|---|---|
| AG-RULE-DATA-001 | data_privacy_risk | medium | high | 0.60 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | data_access:customer_profile | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-DATA-001 | data_privacy_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | logging:customer_profile | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-DATA-001 | data_privacy_risk | medium | high | 0.60 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | data_access:portfolio_notes | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-REG-001 | regulatory_risk | medium | low | 0.41 | NIST-AI-RMF-GOVERN, NIST-AI-RMF-MAP | 2 | data_access:portfolio_notes | Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Document third-party responsibilities, data boundaries, incident handling, and service expectations.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow. |
| AG-RULE-DATA-001 | data_privacy_risk | medium | medium | 0.50 | OWASP-LLM02-2025, NIST-AI-RMF-MAP | 2 | logging:portfolio_notes | Redact or mask personal data before model processing.; Define and enforce data retention and deletion policy.; Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.; Define controls for records that may be subject to regulated business processes.; Track data sources, transformations, outputs, and retention paths used by the agent workflow.; Restrict and monitor access to vector stores or long-term memory containing sensitive content.; Sanitize generated outputs before display, storage, or external transmission. |
| AG-RULE-MODEL-001 | model_risk | low | medium | 0.34 | NIST-AI-RMF-MEASURE | 1 | evaluation | Run task-specific quality, hallucination, and regression tests.; Maintain a model or system card describing intended use, limitations, evaluation results, and known risks.; Run structured red-team exercises against prompt injection, tool misuse, data leakage, and unsafe outputs.; Define fallback behavior when the agent is uncertain or tools fail.; Require sources for factual claims. |

## Detailed Findings
### Sensitive data controls are incomplete
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / high / 0.60
- Affected component: data_access:customer_profile
- Evidence:
  - Data category 'customer_profile' is marked 'personal'.
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
### Input/output logs may capture unredacted sensitive data
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: logging:customer_profile
- Evidence:
  - input_output_logging is true for a workflow with sensitive data.
  - Data category 'customer_profile' has pii_redaction=false.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Sensitive data controls are incomplete
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / high / 0.60
- Affected component: data_access:portfolio_notes
- Evidence:
  - Data category 'portfolio_notes' is marked 'financial'.
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
- Severity / likelihood / score: medium / low / 0.41
- Affected component: data_access:portfolio_notes
- Evidence:
  - Data sensitivity is 'financial'.
  - Privacy controls missing: retention policy, PII redaction.
- Why it matters: Financial or regulated data increases the need for controlled records, monitoring, and review.
- Recommended controls:
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Document third-party responsibilities, data boundaries, incident handling, and service expectations.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
### Input/output logs may capture unredacted sensitive data
- Rule ID: `AG-RULE-DATA-001`
- Risk tag: `data_privacy_risk`
- Framework refs: OWASP-LLM02-2025, NIST-AI-RMF-MAP
- Severity / likelihood / score: medium / medium / 0.50
- Affected component: logging:portfolio_notes
- Evidence:
  - input_output_logging is true for a workflow with sensitive data.
  - Data category 'portfolio_notes' has pii_redaction=false.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls:
  - Redact or mask personal data before model processing.
  - Define and enforce data retention and deletion policy.
  - Assess privacy impact for personal, financial, confidential, or regulated data in the workflow.
  - Define controls for records that may be subject to regulated business processes.
  - Track data sources, transformations, outputs, and retention paths used by the agent workflow.
  - Restrict and monitor access to vector stores or long-term memory containing sensitive content.
  - Sanitize generated outputs before display, storage, or external transmission.
### Model evaluation coverage is incomplete
- Rule ID: `AG-RULE-MODEL-001`
- Risk tag: `model_risk`
- Framework refs: NIST-AI-RMF-MEASURE
- Severity / likelihood / score: low / medium / 0.34
- Affected component: evaluation
- Evidence:
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
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Data category 'customer_profile' is marked 'personal'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Missing: retention policy, PII redaction. |
| AG-RULE-DATA-001 | Input/output logs may capture unredacted sensitive data | input_output_logging is true for a workflow with sensitive data. |
| AG-RULE-DATA-001 | Input/output logs may capture unredacted sensitive data | Data category 'customer_profile' has pii_redaction=false. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Data category 'portfolio_notes' is marked 'financial'. |
| AG-RULE-DATA-001 | Sensitive data controls are incomplete | Missing: retention policy, PII redaction. |
| AG-RULE-REG-001 | Regulated or financial data exposure | Data sensitivity is 'financial'. |
| AG-RULE-REG-001 | Regulated or financial data exposure | Privacy controls missing: retention policy, PII redaction. |
| AG-RULE-DATA-001 | Input/output logs may capture unredacted sensitive data | input_output_logging is true for a workflow with sensitive data. |
| AG-RULE-DATA-001 | Input/output logs may capture unredacted sensitive data | Data category 'portfolio_notes' has pii_redaction=false. |
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
- `retention_policy`: Define and enforce data retention and deletion policy.
- `pii_redaction`: Redact or mask personal data before model processing.
- `output_sanitization`: Sanitize generated outputs before display, storage, or external transmission.
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
- Classify sensitive input fields, redact personal data where possible, and document retention for each data category.
- Define and enforce a retention policy for inputs, outputs, logs, and memory records.
- Redact or mask personal and financial identifiers before model processing or long-term storage.
- Sanitize generated outputs before storage, display, or external transmission.
- Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.
- Run structured red-team tests for prompt injection, data leakage, and tool misuse.
- Require source attribution for financial summaries and portfolio-related factual claims.

## Assumptions and Limitations
- This assessment uses deterministic rules over the provided workflow JSON.
- It does not inspect live production systems, emails, brokers, CRM systems, or real customer records.
- It does not certify security, compliance, legal suitability, financial suitability, or investment suitability.
- Risk scores support portfolio demonstration and technical review; they are not regulatory ratings.

## Disclaimer
This assessment is a technical prototype for AI agent governance review. It is not legal, compliance, financial, investment, or security certification advice.