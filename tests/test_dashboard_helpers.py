from agentguard.dashboard.helpers import filter_findings, findings_to_dataframe


def test_dashboard_helpers_handle_empty_findings():
    assert filter_findings([], severities=["high"]) == []
    assert findings_to_dataframe([]).empty
