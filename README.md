# AgentGuard AI

[![tests](https://github.com/Justin-147/agentguard-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/Justin-147/agentguard-ai/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

AgentGuard AI is a local-first AI agent risk auditor. It evaluates structured descriptions of agent workflows, identifies tool-use, data, oversight, auditability, model, operational, cybersecurity, regulatory, and third-party risks, and generates evidence-backed governance recommendations.

V0.2 is deterministic, reproducible, and API-key-free. It adds workflow validation, config validation, rule IDs, framework references, score explanations, safer reports, CI, schema export, and a richer Streamlit dashboard.

## What It Does

- Loads synthetic AI agent workflow descriptions from JSON.
- Assesses tool permissions, external actions, sensitive data, human oversight, logging, memory, evaluation, and deployment controls.
- Produces deterministic risk findings with rule IDs, framework references, severity, likelihood, evidence, scores, and recommended controls.
- Generates Markdown, HTML, and JSON assessment reports.
- Validates workflow inputs and project configuration.
- Provides a Streamlit dashboard with filters, comparison view, controls, framework mapping, raw JSON, and Markdown preview.
- Runs fully offline without API keys.

## What It Does Not Do

- It is not a SaaS product.
- It does not include login, payment, or multi-user features.
- It does not connect to real Gmail, Outlook, broker, trading, CRM, or customer systems.
- It does not browse the web or process private customer data.
- It does not provide legal, compliance, financial, investment, or security certification advice.

## Quick Start

```powershell
cd agentguard-ai
python -m pip install -e ".[dev]"
python -m agentguard.main assess --case financial_advisor_copilot
```

Reproducible output:

```powershell
python -m agentguard.main assess --case financial_advisor_copilot --as-of 2026-07-06 --output-root .tmp/demo-output
```

## CLI Commands

```powershell
python -m agentguard.main list-cases
python -m agentguard.main validate
python -m agentguard.main validate-workflow --input examples/workflows/high_risk_autonomous_agent.json
python -m agentguard.main assess --case high_risk_autonomous_agent --as-of 2026-07-06 --output-root .tmp/demo-output
python -m agentguard.main assess-all --as-of 2026-07-06 --output-root .tmp/demo-output
python -m agentguard.main export-schema --output docs/workflow_schema.json
```

Reports are written under:

```text
<output-root>/reports/json/
<output-root>/reports/markdown/
<output-root>/reports/html/
```

## Dashboard

```powershell
streamlit run src/agentguard/dashboard/app.py
```

The dashboard includes case search, severity and risk tag filters, score threshold filtering, framework mapping, control descriptions, raw JSON preview, Markdown preview, and demo case comparison.

## Demo Cases

- `financial_advisor_copilot`: Medium-risk wealth management assistant that handles personal and financial data but cannot trade or send messages.
- `customer_support_email_agent`: High-risk support workflow that can send outbound emails without every-action approval.
- `market_intelligence_agent`: Medium-risk public-source research assistant.
- `developer_code_agent`: High-risk coding agent with file-write and command-execution permissions.
- `high_risk_autonomous_agent`: Critical-risk autonomous workflow with sensitive data, external actions, transactions, weak logging, and no approval gates.

## Documentation

- [Methodology](docs/methodology.md)
- [Workflow Schema](docs/workflow_schema.md)
- [Risk Taxonomy](docs/risk_taxonomy.md)
- [Control Library](docs/control_library.md)
- [Framework Mapping](docs/framework_mapping.md)
- [Safety Boundaries](docs/safety_boundaries.md)
- [Roadmap](docs/roadmap.md)

## Sample Reports

Curated sample Markdown reports live in [examples/sample_reports](examples/sample_reports), and JSON outputs live in [examples/sample_outputs](examples/sample_outputs).

## Tests

```powershell
ruff check .
python -m compileall src tests scripts
mypy src/agentguard
pytest
python scripts/run_demo.py
```

## Disclaimer

AgentGuard AI is a portfolio prototype. It does not provide legal, compliance, financial, investment, or security certification advice.
