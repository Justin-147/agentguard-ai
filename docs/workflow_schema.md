# Workflow Schema

Workflow files describe an AI agent workflow in JSON. The canonical machine-readable schema is generated from Pydantic:

```powershell
python -m agentguard.main export-schema --output docs/workflow_schema.json
```

Required sections include tools, data access, external actions, human oversight, logging, memory, evaluation, and deployment.
