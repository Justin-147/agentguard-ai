"""Streamlit dashboard for AgentGuard AI."""

from __future__ import annotations

import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
SRC_DIR = CURRENT_FILE.parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import streamlit as st

from agentguard.assessment.normalize import load_demo_workflow
from agentguard.assessment.report_builder import build_markdown_report
from agentguard.assessment.risk_engine import assess_workflow
from agentguard.config import load_demo_cases


st.set_page_config(page_title="AgentGuard AI", layout="wide")

st.title("AgentGuard AI")

cases = load_demo_cases()
case_names = list(cases.keys())
selected_case = st.sidebar.selectbox(
    "Workflow",
    case_names,
    format_func=lambda name: cases[name]["title"],
)

workflow = load_demo_workflow(selected_case)
result = assess_workflow(workflow)

score_col, level_col, finding_col = st.columns(3)
score_col.metric("Overall Score", f"{result.overall_score:.2f}")
level_col.metric("Overall Risk", result.overall_risk_level)
finding_col.metric("Findings", len(result.findings))

findings_df = pd.DataFrame([finding.model_dump() for finding in result.findings])

left, right = st.columns(2)
with left:
    st.subheader("Risk Tags")
    if findings_df.empty:
        st.info("No findings generated.")
    else:
        st.bar_chart(findings_df["risk_tag"].value_counts())

with right:
    st.subheader("Severity")
    if findings_df.empty:
        st.info("No severity distribution available.")
    else:
        st.bar_chart(findings_df["severity"].value_counts())

st.subheader("Findings")
if findings_df.empty:
    st.info("No findings generated.")
else:
    st.dataframe(
        findings_df[
            [
                "risk_tag",
                "title",
                "severity",
                "likelihood",
                "risk_score",
                "affected_component",
                "recommended_controls",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

st.subheader("Recommended Controls")
if result.control_gaps:
    st.write(", ".join(result.control_gaps))
else:
    st.write("No control gaps identified.")

st.subheader("Markdown Report")
st.markdown(build_markdown_report(workflow, result))
