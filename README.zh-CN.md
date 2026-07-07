# AgentGuard AI

[![tests](https://github.com/Justin-147/agentguard-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/Justin-147/agentguard-ai/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

AgentGuard AI 是一个本地优先的 AI Agent 风险审计原型。它读取结构化 workflow JSON，识别工具权限、外部动作、数据隐私、人工监督、可审计性、模型、运营、网络安全、监管和第三方风险，并生成带证据的治理建议。

V0.2 保持 deterministic、local-first、no API key。新增 workflow 校验、配置校验、规则 ID、框架映射、评分解释、更安全的报告、CI、schema 导出和更完整的 Streamlit dashboard。

## 它能做什么

- 读取合成 AI Agent workflow JSON。
- 审查工具权限、外部动作、敏感数据、人工审批、日志、记忆、评估和部署控制。
- 生成带 rule ID、framework refs、严重性、可能性、证据、评分和推荐控制的风险发现。
- 输出 Markdown、HTML 和 JSON 报告。
- 校验 workflow 输入和项目配置。
- 提供带筛选、对比、控制库、框架映射、原始 JSON 和 Markdown 预览的 dashboard。
- 完全本地运行，不需要 API key。

## 它不做什么

- 不是 SaaS 产品。
- 不包含登录、支付或多用户系统。
- 不连接真实 Gmail、Outlook、券商、交易、CRM 或客户系统。
- 不处理真实客户隐私数据。
- 不提供法律、合规、金融、投资或安全认证建议。

## 快速开始

```powershell
cd agentguard-ai
python -m pip install -e ".[dev]"
python -m agentguard.main assess --case financial_advisor_copilot
```

可复现输出：

```powershell
python -m agentguard.main assess --case financial_advisor_copilot --as-of 2026-07-06 --output-root .tmp/demo-output
```

## CLI 命令

```powershell
python -m agentguard.main list-cases
python -m agentguard.main validate
python -m agentguard.main validate-workflow --input examples/workflows/high_risk_autonomous_agent.json
python -m agentguard.main assess --case high_risk_autonomous_agent --as-of 2026-07-06 --output-root .tmp/demo-output
python -m agentguard.main assess-all --as-of 2026-07-06 --output-root .tmp/demo-output
python -m agentguard.main export-schema --output docs/workflow_schema.json
```

报告输出结构：

```text
<output-root>/reports/json/
<output-root>/reports/markdown/
<output-root>/reports/html/
```

## Dashboard

```powershell
streamlit run src/agentguard/dashboard/app.py
```

Dashboard 包含 case 搜索、严重性筛选、risk tag 筛选、分数阈值、框架映射、控制说明、原始 JSON、Markdown 预览和 demo case 对比。

## Demo Cases

- `financial_advisor_copilot`：中等风险财富管理助手，处理个人和金融数据，但不能交易或发送外部消息。
- `customer_support_email_agent`：高风险客服邮件 Agent，可以发送外部邮件，但没有每次动作审批。
- `market_intelligence_agent`：中等风险公开信息研究助手。
- `developer_code_agent`：高风险代码 Agent，具备文件写入和命令执行能力。
- `high_risk_autonomous_agent`：关键风险自治 Agent，包含敏感数据、外部动作、交易、弱日志和缺失审批。

## 文档

- [Methodology](docs/methodology.md)
- [Workflow Schema](docs/workflow_schema.md)
- [Risk Taxonomy](docs/risk_taxonomy.md)
- [Control Library](docs/control_library.md)
- [Framework Mapping](docs/framework_mapping.md)
- [Safety Boundaries](docs/safety_boundaries.md)
- [Roadmap](docs/roadmap.md)

## 样例报告

精选 Markdown 样例位于 [examples/sample_reports](examples/sample_reports)，JSON 样例位于 [examples/sample_outputs](examples/sample_outputs)。

## 测试

```powershell
ruff check .
python -m compileall src tests scripts
mypy src/agentguard
pytest
python scripts/run_demo.py
```

## 免责声明

AgentGuard AI 是作品集原型。它不提供法律、合规、金融、投资或安全认证建议。
