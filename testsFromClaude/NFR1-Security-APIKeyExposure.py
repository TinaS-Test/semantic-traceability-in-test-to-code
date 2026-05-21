# ============================================================
# Test Category  : Security / Static Analysis
# Requirement(s) : Doc 1 – NFR1.2 (no hardcoded API keys in app.py),
#                  NFR1.1 (internal-only communication)
# ============================================================

import re
import requests
import pytest

APP_PY_PATH = "/opt/tina/app.py"

# Pattern that matches a Gemini API key format (AIza...)
GEMINI_KEY_PATTERN = re.compile(r"AIza[0-9A-Za-z\-_]{35}")


def test_api_key_not_hardcoded_in_source():
    """
    NFR1.2: app.py must not contain a hardcoded Gemini API key.
    The key must only be loaded via os.environ or python-dotenv.
    """
    with open(APP_PY_PATH, "r") as source_file:
        source_code = source_file.read()

    match = GEMINI_KEY_PATTERN.search(source_code)
    assert match is None, (
        f"SECURITY VIOLATION: Hardcoded Gemini API key found in app.py at position {match.start()}."
    )


def test_api_key_not_exposed_in_http_response():
    """
    NFR1.2: The Gemini API key must not appear in any HTTP response from the application.
    Checks the translation endpoint response headers and body.
    """
    response = requests.post(
        "https://tina.ethernettrip.com/translate",
        headers={"Authorization": "Bearer <valid-token-from-fixture>"},
        json={"text": "Säkerhetstestning"}
    )

    full_response_text = response.text + str(response.headers)
    match = GEMINI_KEY_PATTERN.search(full_response_text)
    assert match is None, (
        "SECURITY VIOLATION: Gemini API key pattern detected in HTTP response."
    )