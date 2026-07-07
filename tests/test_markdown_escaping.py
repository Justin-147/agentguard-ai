from agentguard.assessment.report_builder import build_html_report
from agentguard.writers.formatting import fmt_score, md_cell, safe_text


def test_md_cell_escapes_pipe_newline_and_html():
    value = " hello | world\n<script> "

    assert md_cell(value) == "hello \\| world &lt;script&gt;"


def test_html_report_escapes_title():
    html = build_html_report("# Title", "Agent <script>alert(1)</script>")

    assert "<html" in html.lower()
    assert "Agent &lt;script&gt;alert(1)&lt;/script&gt;" in html


def test_safe_text_and_fmt_score():
    assert safe_text(" hello\n<script> ") == "hello &lt;script&gt;"
    assert fmt_score("0.456") == "0.46"
    assert fmt_score(None) == ""
