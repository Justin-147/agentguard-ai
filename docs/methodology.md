# Methodology

AgentGuard AI uses deterministic rules over a structured workflow JSON file. It reviews tool permissions, data sensitivity, external actions, human oversight, logging, memory, evaluation controls, and deployment controls.

The system does not call external LLM APIs, connect to live systems, or inspect real customer data. Findings are generated from explicit workflow fields and mapped to controls and framework references.

Scoring uses:

```text
overall_score =
  0.50 * max_finding_score
+ 0.30 * mean_top_5_score
+ 0.20 * control_gap_density
```

Critical overrides raise the level when high-impact autonomy, financial action, weak logging, sensitive memory, or customer-facing exposure is present.
