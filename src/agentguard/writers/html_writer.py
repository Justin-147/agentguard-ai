"""HTML report writer."""

from __future__ import annotations

from pathlib import Path


def write_html_report(html_text: str, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    return path
