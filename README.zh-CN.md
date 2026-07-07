# AgentGuard AI

AgentGuard AI 是一个本地优先的 AI Agent 风险审计原型。它会读取结构化的 Agent 工作流描述，识别工具权限、外部动作、数据隐私、人工监督、可审计性、模型质量、运营韧性和网络安全风险，并生成带证据的治理建议。

这个项目定位为求职作品集项目，适合展示 AI 治理、模型风险、运营风险、RegTech、金融服务 AI 风险和 AI 解决方案咨询相关能力。

## 它能做什么

- 从 JSON 读取 AI Agent 工作流描述。
- 审查工具权限、外部动作、敏感数据、人工审批、日志、记忆、评估和部署控制。
- 生成确定性的风险发现，包括严重性、可能性、证据、评分和推荐控制。
- 输出 Markdown、HTML 和 JSON 评估报告。
- 提供一个简单的 Streamlit dashboard，用于查看 workflow、风险分布、发现列表和报告。
- V1 完全本地运行，不需要 API key。

## 它不做什么

- 不是 SaaS 产品。
- 不包含登录、支付或多用户系统。
- 不连接真实 Gmail、Outlook、券商、交易或客户系统。
- 不进行无限制网页浏览，也不处理真实客户隐私数据。
- 不提供法律、合规、金融、投资或安全认证建议。

## 求职相关性

AgentGuard AI 可以展示：

- AI 治理与可审计性思维。
- Agent 工作流风险评估能力。
- 工具调用与权限风险分析。
- 运营韧性、回滚和事件响应控制设计。
- 金融服务和 RegTech 风险意识。
- 面向业务和技术干系人的报告生成能力。

## 架构

```text
config/
  risk_taxonomy.yaml       风险分类
  control_library.yaml     控制库与风险映射
  demo_cases.yaml          Demo workflow 索引
  report_template.md       Markdown 报告模板

src/agentguard/
  models.py                Pydantic 数据模型
  assessment/              规则引擎、评分、控制映射、报告生成
  writers/                 Markdown、HTML、JSON 写入器
  dashboard/app.py         Streamlit dashboard
  main.py                  CLI 入口

examples/
  workflows/               Demo workflow JSON 文件
  sample_reports/          精选 Markdown 样例报告
  sample_outputs/          精选 JSON 样例输出
```

## 快速开始

```powershell
cd agentguard-ai
python -m pip install -e ".[dev]"
python -m agentguard.main assess --case financial_advisor_copilot
```

预期输出：

```text
json: reports/json/financial_advisor_copilot_assessment.json
markdown: reports/markdown/financial_advisor_copilot_assessment.md
html: reports/html/financial_advisor_copilot_assessment.html
overall_risk_level: Medium
overall_score: 0.49
```

## CLI 命令

评估 demo case：

```powershell
python -m agentguard.main assess --case financial_advisor_copilot
python -m agentguard.main assess --case high_risk_autonomous_agent
```

从输入文件评估：

```powershell
python -m agentguard.main assess --input examples/workflows/high_risk_autonomous_agent.json
```

## Dashboard

```powershell
streamlit run src/agentguard/dashboard/app.py
```

Dashboard 包含 workflow 选择器、总体风险等级、总分、风险标签分布、严重性分布、风险发现表、推荐控制和 Markdown 报告渲染。

## Demo Cases

- `financial_advisor_copilot`：中等风险财富管理助手，处理个人和金融数据，但不能交易或发送外部消息。
- `customer_support_email_agent`：客服邮件 Agent，可以发送外部邮件，但没有每次动作审批。
- `market_intelligence_agent`：低到中等风险的公开信息研究助手。
- `developer_code_agent`：具备文件写入和命令执行能力的代码 Agent。
- `high_risk_autonomous_agent`：刻意设计的高风险自治 Agent，包含敏感数据、外部动作、交易、弱日志和缺失审批。

## 样例报告

- [Financial Advisor Copilot Markdown](examples/sample_reports/financial_advisor_copilot_assessment.md)
- [High Risk Autonomous Agent Markdown](examples/sample_reports/high_risk_autonomous_agent_assessment.md)
- [Financial Advisor Copilot JSON](examples/sample_outputs/financial_advisor_copilot_assessment.json)
- [High Risk Autonomous Agent JSON](examples/sample_outputs/high_risk_autonomous_agent_assessment.json)

## 测试

```powershell
pytest
```

## 免责声明

AgentGuard AI 是作品集原型。它不提供法律、合规、金融、投资或安全认证建议。
