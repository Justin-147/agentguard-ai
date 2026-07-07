"""Build Markdown, HTML, and JSON assessment reports."""

from __future__ import annotations

from pathlib import Path

import markdown as markdown_lib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from agentguard.config import report_template_path, reports_dir
from agentguard.models import AgentWorkflow, AssessmentResult
from agentguard.writers.html_writer import write_html_report
from agentguard.writers.json_writer import write_json_report
from agentguard.writers.markdown_writer import write_markdown_report


def build_markdown_report(workflow: AgentWorkflow, result: AssessmentResult) -> str:
    template_path = report_template_path()
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    ranked_findings = sorted(result.findings, key=lambda item: item.risk_score, reverse=True)
    top_risk_drivers: list[str] = []
    for finding in ranked_findings:
        if finding.risk_tag not in top_risk_drivers:
            top_risk_drivers.append(finding.risk_tag)
        if len(top_risk_drivers) == 5:
            break
    data_categories = [
        f"{access.data_category} ({access.sensitivity})"
        for access in workflow.data_access
    ]
    return template.render(
        workflow=workflow,
        result=result,
        top_risk_drivers=top_risk_drivers,
        urgent_control_gaps=result.control_gaps[:5],
        data_categories=data_categories,
        generated_at=result.generated_at.isoformat(),
    )


def build_html_report(markdown_text: str, title: str) -> str:
    body = markdown_lib.markdown(markdown_text, extensions=["tables", "toc"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172033;
      --muted: #5d667a;
      --line: #d9dee8;
      --panel: #f7f9fc;
      --accent: #0f766e;
    }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: #ffffff;
      line-height: 1.55;
    }}
    main {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }}
    h1, h2, h3 {{
      line-height: 1.25;
    }}
    h1 {{
      border-bottom: 3px solid var(--accent);
      padding-bottom: 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0 24px;
      font-size: 14px;
    }}
    th, td {{
      border: 1px solid var(--line);
      padding: 10px;
      vertical-align: top;
    }}
    th {{
      background: var(--panel);
      text-align: left;
    }}
    code {{
      background: var(--panel);
      padding: 2px 5px;
      border-radius: 4px;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""


def generate_reports(
    workflow: AgentWorkflow,
    result: AssessmentResult,
    output_root: Path | None = None,
) -> dict[str, Path]:
    root = output_root or reports_dir()
    report_name = f"{workflow.id}_assessment"
    markdown_text = build_markdown_report(workflow, result)
    html_text = build_html_report(markdown_text, f"AgentGuard AI Assessment | {workflow.name}")
    paths = {
        "json": root / "json" / f"{report_name}.json",
        "markdown": root / "markdown" / f"{report_name}.md",
        "html": root / "html" / f"{report_name}.html",
    }
    write_json_report(result, paths["json"])
    write_markdown_report(markdown_text, paths["markdown"])
    write_html_report(html_text, paths["html"])
    return paths
