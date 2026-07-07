"""Configuration loading helpers for AgentGuard AI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def config_dir() -> Path:
    return project_root() / "config"


def examples_dir() -> Path:
    return project_root() / "examples"


def reports_dir() -> Path:
    return project_root() / "reports"


def workflows_dir() -> Path:
    return examples_dir() / "workflows"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return data


def load_risk_taxonomy() -> dict[str, Any]:
    return load_yaml(config_dir() / "risk_taxonomy.yaml")


def load_control_library() -> dict[str, Any]:
    return load_yaml(config_dir() / "control_library.yaml")


def load_framework_mapping() -> dict[str, Any]:
    return load_yaml(config_dir() / "framework_mapping.yaml")


def load_rules() -> dict[str, Any]:
    return load_yaml(config_dir() / "rules.yaml").get("rules", {})


def load_demo_cases() -> dict[str, Any]:
    return load_yaml(config_dir() / "demo_cases.yaml").get("demo_cases", {})


def report_template_path() -> Path:
    return config_dir() / "report_template.md"
