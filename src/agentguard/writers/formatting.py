"""Formatting helpers for generated reports."""

from __future__ import annotations

import re
from html import escape


def md_cell(value: object) -> str:
    """Render a value safely inside a Markdown table cell."""

    if value is None:
        return ""
    if isinstance(value, list | tuple | set):
        text = ", ".join(str(item) for item in value)
    else:
        text = str(value)
    text = escape(text, quote=False)
    text = text.replace("\r", " ").replace("\n", " ")
    text = text.replace("|", r"\|")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def safe_text(value: object) -> str:
    """Escape and normalize text for safe display."""

    if value is None:
        return ""
    text = escape(str(value), quote=True)
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fmt_score(value: object) -> str:
    """Format numeric scores consistently in reports."""

    try:
        return f"{float(str(value)):.2f}"
    except (TypeError, ValueError):
        return ""
