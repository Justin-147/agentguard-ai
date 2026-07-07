"""JSON report writer."""

from __future__ import annotations

import json
from pathlib import Path

from agentguard.models import AssessmentResult


def write_json_report(result: AssessmentResult, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = result.model_dump(mode="json")
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
