"""Command-line interface for AgentGuard AI."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime, time
from pathlib import Path

from agentguard.assessment.normalize import load_demo_workflow, load_workflow
from agentguard.assessment.report_builder import generate_reports
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.config import load_demo_cases, project_root
from agentguard.models import AgentWorkflow, AssessmentResult
from agentguard.validation.config_validator import validate_config, write_issues
from agentguard.validation.workflow_validator import validate_workflow_file


def parse_as_of(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        if len(value) == 10:
            parsed = datetime.combine(datetime.fromisoformat(value).date(), time.min)
        else:
            parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "--as-of must use YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS, "
            "or YYYY-MM-DDTHH:MM:SS+HH:MM format."
        ) from exc
    if parsed.tzinfo is None:
        return parsed
    return parsed.astimezone(UTC).replace(tzinfo=None)


def assess(
    *,
    case_name: str | None = None,
    input_path: Path | None = None,
    output_root: Path | None = None,
    generated_at: datetime | None = None,
) -> tuple[AgentWorkflow, AssessmentResult, dict[str, Path]]:
    if case_name:
        workflow = load_demo_workflow(case_name)
    elif input_path:
        workflow = load_workflow(input_path)
    else:
        raise ValueError("Either case_name or input_path is required.")

    result = assess_workflow(workflow, generated_at=generated_at)
    paths = generate_reports(workflow, result, output_root)
    return workflow, result, paths


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(project_root()).as_posix()
    except ValueError:
        return path.as_posix()


def _print_assessment(result: AssessmentResult, paths: dict[str, Path]) -> None:
    print(f"json: {_display_path(paths['json'])}")
    print(f"markdown: {_display_path(paths['markdown'])}")
    print(f"html: {_display_path(paths['html'])}")
    print(f"overall_risk_level: {result.overall_risk_level}")
    print(f"overall_score: {result.overall_score:.2f}")


def _add_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--output-root",
        dest="output_root",
        type=Path,
        default=None,
        help="Output root. Reports are written under <output-root>/reports/.",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_root",
        type=Path,
        default=None,
        help="Deprecated alias for --output-root.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentguard",
        description="Assess AI agent workflows for governance and operational risk.",
    )
    subparsers = parser.add_subparsers(dest="command")

    assess_parser = subparsers.add_parser(
        "assess", help="Assess a demo case or workflow JSON file."
    )
    source = assess_parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--case", dest="case_name", help="Demo case name from config/demo_cases.yaml."
    )
    source.add_argument("--input", dest="input_path", type=Path, help="Path to workflow JSON.")
    assess_parser.add_argument("--as-of", dest="as_of", type=parse_as_of, default=None)
    _add_output_args(assess_parser)

    assess_all_parser = subparsers.add_parser("assess-all", help="Assess every demo workflow.")
    assess_all_parser.add_argument("--as-of", dest="as_of", type=parse_as_of, default=None)
    _add_output_args(assess_all_parser)

    subparsers.add_parser("list-cases", help="List available demo cases.")
    subparsers.add_parser("validate", help="Validate AgentGuard configuration.")

    validate_workflow_parser = subparsers.add_parser(
        "validate-workflow", help="Validate one workflow JSON file."
    )
    validate_workflow_parser.add_argument("--input", type=Path, required=True)

    export_schema_parser = subparsers.add_parser(
        "export-schema", help="Export AgentWorkflow JSON schema."
    )
    export_schema_parser.add_argument("--output", type=Path, required=True)

    return parser


def _handle_assess(args: argparse.Namespace) -> int:
    _, result, paths = assess(
        case_name=args.case_name,
        input_path=args.input_path,
        output_root=args.output_root,
        generated_at=args.as_of,
    )
    _print_assessment(result, paths)
    return 0


def _handle_assess_all(args: argparse.Namespace) -> int:
    cases = load_demo_cases()
    for case_name in cases:
        _, result, paths = assess(
            case_name=case_name,
            output_root=args.output_root,
            generated_at=args.as_of,
        )
        print(f"case: {case_name}")
        _print_assessment(result, paths)
    return 0


def _handle_list_cases() -> int:
    for case_name, case in load_demo_cases().items():
        title = case.get("title", "")
        expected = case.get("expected_risk", "Unknown")
        print(f"{case_name:<32} title=\"{title}\" expected={expected}")
    return 0


def _handle_validate() -> int:
    issues = validate_config()
    print(write_issues(issues))
    return 1 if any(issue.level == "error" for issue in issues) else 0


def _handle_validate_workflow(args: argparse.Namespace) -> int:
    issues = validate_workflow_file(args.input)
    print(write_issues(issues))
    return 1 if any(issue.level == "error" for issue in issues) else 0


def _handle_export_schema(args: argparse.Namespace) -> int:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(AgentWorkflow.model_json_schema(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"schema: {_display_path(args.output)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "assess":
        return _handle_assess(args)
    if args.command == "assess-all":
        return _handle_assess_all(args)
    if args.command == "list-cases":
        return _handle_list_cases()
    if args.command == "validate":
        return _handle_validate()
    if args.command == "validate-workflow":
        return _handle_validate_workflow(args)
    if args.command == "export-schema":
        return _handle_export_schema(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
