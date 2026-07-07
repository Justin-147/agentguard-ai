# AgentGuard AI

AgentGuard AI is a local-first AI agent risk auditor. It evaluates structured descriptions of agent workflows, identifies tool-use, data, oversight, auditability, model, operational, and cybersecurity risks, and generates evidence-backed governance recommendations.

It is designed as a recruitment-ready portfolio project for AI governance, model risk, operational risk, RegTech, financial services AI risk, and AI solution consulting roles.

## What It Does

- Loads structured AI agent workflow descriptions from JSON.
- Assesses tool permissions, external actions, sensitive data, human oversight, logging, memory, evaluation, and deployment controls.
- Produces deterministic risk findings with severity, likelihood, evidence, scores, and recommended controls.
- Generates Markdown, HTML, and JSON assessment reports.
- Provides a simple Streamlit dashboard for workflow comparison and finding review.
- Runs fully offline without API keys.

## What It Does Not Do

- It is not a SaaS product.
- It does not include login, payment, or multi-user features.
- It does not connect to real Gmail, Outlook, broker, trading, or customer systems.
- It does not browse the web or process private customer data.
- It does not provide legal, compliance, financial, investment, or security certification advice.

## Target Job Relevance

AgentGuard AI demonstrates:

- AI governance and auditability thinking.
- Agent workflow risk assessment.
- Tool-use and permission risk analysis.
- Operational resilience and incident-response control design.
- Financial services and RegTech risk awareness.
- Clear report generation for business and technical stakeholders.

## Architecture

```text
config/
  risk_taxonomy.yaml       Risk categories and keywords
  control_library.yaml     Governance controls mapped to risks
  demo_cases.yaml          Demo workflow index
  report_template.md       Markdown report template

src/agentguard/
  models.py                Pydantic workflow and assessment models
  assessment/              Rule engine, scoring, controls, reports
  writers/                 Markdown, HTML, and JSON writers
  dashboard/app.py         Streamlit dashboard
  main.py                  CLI entrypoint

examples/
  workflows/               Demo workflow JSON files
  sample_reports/          Curated sample Markdown reports
  sample_outputs/          Curated sample JSON outputs
```

## Quick Start

```powershell
cd agentguard-ai
python -m pip install -e ".[dev]"
python -m agentguard.main assess --case financial_advisor_copilot
```

Expected CLI output:

```text
json: reports/json/financial_advisor_copilot_assessment.json
markdown: reports/markdown/financial_advisor_copilot_assessment.md
html: reports/html/financial_advisor_copilot_assessment.html
overall_risk_level: Medium
overall_score: 0.49
```

## CLI Commands

Assess a demo case:

```powershell
python -m agentguard.main assess --case financial_advisor_copilot
python -m agentguard.main assess --case high_risk_autonomous_agent
```

Assess from an input file:

```powershell
python -m agentguard.main assess --input examples/workflows/high_risk_autonomous_agent.json
```

## Dashboard

```powershell
streamlit run src/agentguard/dashboard/app.py
```

The dashboard includes a workflow selector, overall risk level, score, risk tag distribution, severity distribution, findings table, recommended controls, and rendered Markdown report.

## Demo Cases

- `financial_advisor_copilot`: Medium-risk wealth management assistant that handles personal and financial data but cannot trade or send messages.
- `customer_support_email_agent`: Customer support workflow that can send outbound emails without every-action approval.
- `market_intelligence_agent`: Low-to-medium-risk public-source research assistant.
- `developer_code_agent`: Coding agent with file-write and command-execution permissions.
- `high_risk_autonomous_agent`: Deliberately high-risk autonomous workflow with sensitive data, external actions, transactions, weak logging, and no approval gates.

## Sample Reports

- [Financial Advisor Copilot Markdown](examples/sample_reports/financial_advisor_copilot_assessment.md)
- [High Risk Autonomous Agent Markdown](examples/sample_reports/high_risk_autonomous_agent_assessment.md)
- [Financial Advisor Copilot JSON](examples/sample_outputs/financial_advisor_copilot_assessment.json)
- [High Risk Autonomous Agent JSON](examples/sample_outputs/high_risk_autonomous_agent_assessment.json)

## Tests

```powershell
pytest
```

## Disclaimer

AgentGuard AI is a portfolio prototype. It does not provide legal, compliance, financial, investment, or security certification advice.
