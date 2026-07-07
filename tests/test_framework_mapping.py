from agentguard.config import load_framework_mapping, load_risk_taxonomy


def test_framework_mapping_risk_tags_exist_in_taxonomy():
    taxonomy_tags = set(load_risk_taxonomy()["risk_tags"])

    for framework in load_framework_mapping()["frameworks"].values():
        assert set(framework["risk_tags"]).issubset(taxonomy_tags)
