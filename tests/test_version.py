from importlib.metadata import version

import agentguard


def test_package_version_matches_project_metadata():
    assert agentguard.__version__ == version("agentguard-ai")
