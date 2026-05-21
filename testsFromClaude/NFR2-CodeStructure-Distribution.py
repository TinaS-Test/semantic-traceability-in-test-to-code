# ============================================================
# Test Category  : Static / Structural
# Requirement(s) : Doc 1 – NFR2.1 (requirements.txt must exist and be maintained)
#                  NFR2.2 (source tracked in GitLab — verified separately via git remote)
# ============================================================

import subprocess
import pytest

REQUIREMENTS_FILE_PATH = "/opt/tina/requirements.txt"

# Minimum expected packages based on the described stack (FR3.1, FR4.1, FR5.2, FR1.3)
REQUIRED_DEPENDENCIES = [
    "flask",       # FR3.1
    "psycopg2",    # FR4.1
    "bcrypt",      # FR1.3
    "python-dotenv", # NFR1.2
    "requests",    # FR3.2 (Gemini API call)
]


def test_dependency_manifest_complete():
    """
    NFR2.1: requirements.txt must exist and declare all core dependencies.
    Missing entries make the environment non-reproducible.
    """
    with open(REQUIREMENTS_FILE_PATH, "r") as req_file:
        content = req_file.read().lower()

    missing = [dep for dep in REQUIRED_DEPENDENCIES if dep not in content]
    assert not missing, (
        f"requirements.txt is missing the following dependencies: {missing}"
    )


def test_gitlab_remote_is_configured():
    """
    NFR2.2: The application source must be version-controlled in GitLab.
    Checks that the git remote points to the correct GitLab host.
    """
    result = subprocess.run(
        ["git", "-C", "/opt/tina", "remote", "-v"],
        capture_output=True, text=True
    )
    assert "gitlab.ethernettrip.com" in result.stdout, (
        "No GitLab remote configured — NFR2.2 not satisfied."
    )