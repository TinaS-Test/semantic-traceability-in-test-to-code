# Test Category:
# Static Security Test

# Requirements Covered:
# NFR1.2

import os

def test_api_key_loaded_from_environment():
    """
    Ensures secrets are externalized.

    Semantic focus:
    protected ("skydd")
    environment variable (".env")
    """

    api_key = os.getenv("GEMINI_API_KEY")

    assert api_key is not None