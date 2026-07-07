# AgentGuard AI Assessment | Financial Advisor Copilot

## Executive Summary
- Overall risk level: **Medium**
- Overall score: **0.49**
- Top risk drivers: data_privacy_risk, regulatory_risk, model_risk
- Most urgent control gaps: pii_redaction, retention_policy, evaluation_suite, fallback_procedure, source_attribution

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
| Generated at | 2026-07-06T07:20:12.997880+00:00 |

## Risk Findings
| Risk | Severity | Likelihood | Score | Affected Component | Recommended Controls |
|---|---|---|---|---|---|
| data_privacy_risk | medium | high | 0.60 | data_access:customer_profile | pii_redaction, retention_policy |
| data_privacy_risk | medium | high | 0.60 | data_access:portfolio_notes | pii_redaction, retention_policy |
| regulatory_risk | medium | low | 0.41 | data_access:portfolio_notes |  |
| model_risk | low | medium | 0.34 | evaluation | evaluation_suite, fallback_procedure, source_attribution |

## Detailed Findings
### Sensitive data controls are incomplete
- Risk tag: `data_privacy_risk`
- Severity / likelihood / score: medium / high / 0.60
- Affected component: data_access:customer_profile
- Evidence:
  - Data category 'customer_profile' is marked 'personal'.
  - Missing: retention policy, PII redaction.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls: pii_redaction, retention_policy
### Sensitive data controls are incomplete
- Risk tag: `data_privacy_risk`
- Severity / likelihood / score: medium / high / 0.60
- Affected component: data_access:portfolio_notes
- Evidence:
  - Data category 'portfolio_notes' is marked 'financial'.
  - Missing: retention policy, PII redaction.
- Why it matters: Sensitive data processing lacks one or more basic privacy controls.
- Recommended controls: pii_redaction, retention_policy
### Regulated or financial data exposure
- Risk tag: `regulatory_risk`
- Severity / likelihood / score: medium / low / 0.41
- Affected component: data_access:portfolio_notes
- Evidence:
  - Data sensitivity is 'financial'.
  - Privacy controls missing: retention policy, PII redaction.
- Why it matters: Financial or regulated data increases the need for controlled records, monitoring, and review.
- Recommended controls: None mapped
### Model evaluation coverage is incomplete
- Risk tag: `model_risk`
- Severity / likelihood / score: low / medium / 0.34
- Affected component: evaluation
- Evidence:
  - Missing evaluation control: hallucination tests.
- Why it matters: The workflow has missing model quality, hallucination, monitoring, or fallback checks.
- Recommended controls: evaluation_suite, fallback_procedure, source_attribution

## Control Gap Summary
### Missing Controls
- pii_redaction
- retention_policy
- evaluation_suite
- fallback_procedure
- source_attribution

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
- Redact or mask personal and financial identifiers before model processing or long-term storage.
- Define and enforce a retention policy for inputs, outputs, logs, and memory records.
- Run a task-specific evaluation suite covering hallucination, regression, and answer-quality checks before release.
- Define fallback behavior for low-confidence outputs, tool failures, and missing evidence.
- Require source attribution for factual claims in generated reports or customer-facing content.

## Disclaimer
This assessment is a technical prototype for AI agent governance review. It is not legal, compliance, financial, or security certification advice.