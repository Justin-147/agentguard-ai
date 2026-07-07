"""Command-line interface for AgentGuard AI."""

from __future__ import annotations

import argparse
from pathlib import Path

from agentguard.assessment.normalize import load_demo_workflow, load_workflow
from agentguard.assessment.report_builder import generate_reports
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.config import project_root, reports_dir
from agentguard.models import AgentWorkflow, AssessmentResult


def assess(
    *,
    case_name: str | None = None,
    input_path: Path | None = None,
    output_root: Path | None = None,
) -> tuple[AgentWorkflow, AssessmentResult, dict[str, Path]]:
    if case_name:
        workflow = load_demo_workflow(case_name)
    elif input_path:
        workflow = load_workflow(input_path)
    else:
        raise ValueError("Either case_name or input_path is required.")

    result = assess_workflow(workflow)
    paths = generate_reports(workflow, result, output_root or reports_dir())
    return workflow, result, paths


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(project_root()).as_posix()
    except ValueError:
        return path.as_posix()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentguard",
        description="Assess AI agent workflows for governance and operational risk.",
    )
    subparsers = parser.add_subparsers(dest="command")

    assess_parser = subparsers.add_parser("assess", help="Assess a demo case or workflow JSON file.")
    source = assess_parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--case", dest="case_name", help="Demo case name from config/demo_cases.yaml.")
    source.add_argument("--input", dest="input_path", type=Path, help="Path to workflow JSON.")
    assess_parser.add_argument(
        "--output-dir",
        dest="output_root",
        type=Path,
        default=None,
        help="Optional output directory for generated reports.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "assess":
        _, result, paths = assess(
            case_name=args.case_name,
            input_path=args.input_path,
            output_root=args.output_root,
        )
        print(f"json: {_display_path(paths['json'])}")
        print(f"markdown: {_display_path(paths['markdown'])}")
        print(f"html: {_display_path(paths['html'])}")
        print(f"overall_risk_level: {result.overall_risk_level}")
        print(f"overall_score: {result.overall_score:.2f}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
