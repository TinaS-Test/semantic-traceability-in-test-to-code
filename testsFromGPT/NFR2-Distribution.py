# Test Category:
# Configuration Test

# Requirements Covered:
# NFR2.1

def test_requirements_file_contains_flask():
    """
    Verifies runtime dependencies
    are maintained centrally.

    Semantic focus:
    maintain ("underhållas")
    reproducibility ("reproducerbarhet")
    """

    with open("requirements.txt") as file:
        content = file.read()

    assert "Flask" in content