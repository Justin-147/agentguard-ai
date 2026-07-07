"""Streamlit dashboard for AgentGuard AI."""

# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
SRC_DIR = CURRENT_FILE.parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.report_builder import build_markdown_report
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.config import load_control_library, load_demo_cases, load_framework_mapping
from agentguard.dashboard.helpers import (
    comparison_dataframe,
    filter_findings,
    findings_to_dataframe,
)

st.set_page_config(page_title="AgentGuard AI", layout="wide")
st.title("AgentGuard AI")

cases = load_demo_cases()
case_search = st.sidebar.text_input("Search cases", "")
case_names = [
    name
    for name, meta in cases.items()
    if case_search.lower() in f"{name} {meta.get('title', '')}".lower()
]
if not case_names:
    st.warning("No demo cases match the search.")
    st.stop()

selected_case = st.sidebar.selectbox(
    "Workflow",
    case_names,
    format_func=lambda name: cases[name]["title"],
)

workflow = load_demo_workflow(selected_case)
result = assess_workflow(workflow)

all_severities = sorted({finding.severity for finding in result.findings})
all_risk_tags = sorted({finding.risk_tag for finding in result.findings})
selected_severities = st.sidebar.multiselect("Severity", all_severities)
selected_risk_tags = st.sidebar.multiselect("Risk tag", all_risk_tags)
min_score = st.sidebar.slider("Minimum finding score", 0.0, 1.0, 0.0, 0.05)

filtered_findings = filter_findings(
    result.findings,
    severities=selected_severities,
    risk_tags=selected_risk_tags,
    min_score=min_score,
)
findings_df = findings_to_dataframe(filtered_findings)

score_col, level_col, finding_col = st.columns(3)
score_col.metric("Overall Score", f"{result.overall_score:.2f}")
level_col.metric("Overall Risk", result.overall_risk_level)
finding_col.metric("Findings", len(result.findings))

(
    overview_tab,
    findings_tab,
    controls_tab,
    frameworks_tab,
    raw_tab,
    report_tab,
    compare_tab,
) = st.tabs(
    [
        "Overview",
        "Findings",
        "Controls",
        "Frameworks",
        "Raw JSON",
        "Markdown Report",
        "Comparison",
    ]
)

with overview_tab:
    left, right = st.columns(2)
    with left:
        st.subheader("Risk Tags")
        if findings_df.empty:
            st.info("No findings match the current filters.")
        else:
            st.bar_chart(findings_df["risk_tag"].value_counts())
    with right:
        st.subheader("Severity")
        if findings_df.empty:
            st.info("No severity distribution available.")
        else:
            st.bar_chart(findings_df["severity"].value_counts())

with findings_tab:
    st.subheader("Findings")
    if findings_df.empty:
        st.info("No findings match the current filters.")
    else:
        st.dataframe(
            findings_df[
                [
                    "rule_id",
                    "risk_tag",
                    "title",
                    "severity",
                    "likelihood",
                    "risk_score",
                    "affected_component",
                    "framework_refs",
                    "recommended_controls",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

with controls_tab:
    st.subheader("Control Descriptions")
    controls = load_control_library().get("controls", {})
    st.dataframe(
        [
            {
                "control": control_id,
                "description": control.get("description", ""),
                "mitigates": ", ".join(control.get("mitigates", [])),
            }
            for control_id, control in controls.items()
        ],
        use_container_width=True,
        hide_index=True,
    )

with frameworks_tab:
    st.subheader("Framework Mapping")
    frameworks = load_framework_mapping().get("frameworks", {})
    st.dataframe(
        [
            {
                "framework": framework_id,
                "name": framework.get("name", ""),
                "risk_tags": ", ".join(framework.get("risk_tags", [])),
            }
            for framework_id, framework in frameworks.items()
        ],
        use_container_width=True,
        hide_index=True,
    )

with raw_tab:
    st.subheader("Raw Assessment JSON")
    st.json(result.model_dump(mode="json"))

with report_tab:
    st.subheader("Markdown Report")
    st.markdown(build_markdown_report(workflow, result))

with compare_tab:
    st.subheader("Demo Case Comparison")
    workflows = [load_demo_workflow(case_name) for case_name in cases]
    st.dataframe(comparison_dataframe(workflows), use_container_width=True, hide_index=True)
