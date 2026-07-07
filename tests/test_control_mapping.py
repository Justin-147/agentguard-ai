from agentguard.assessment.control_mapper import controls_for_risk_tag


def test_regulatory_and_third_party_risks_have_controls():
    assert controls_for_risk_tag("regulatory_risk")
    assert controls_for_risk_tag("third_party_risk")
