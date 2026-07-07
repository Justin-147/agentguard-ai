"""Workflow loading and normalization helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path

from agentguard.config import load_demo_cases, project_root
from agentguard.models import AgentWorkflow


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return normalized.strip("_")


def load_workflow(path: Path | str) -> AgentWorkflow:
    workflow_path = Path(path)
    with workflow_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    return AgentWorkflow.model_validate(payload)


def load_demo_workflow(case_name: str) -> AgentWorkflow:
    cases = load_demo_cases()
    if case_name not in cases:
        available = ", ".join(sorted(cases))
        raise KeyError(f"Unknown demo case '{case_name}'. Available cases: {available}")
    return load_workflow(project_root() / cases[case_name]["path"])
