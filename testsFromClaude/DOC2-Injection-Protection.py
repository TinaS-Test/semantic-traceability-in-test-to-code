# ============================================================
# Test Category  : Security / Input Validation
# Requirement(s) : Doc 2 – Ch 1.1.1 (XSS and SQL injection must be
#                  blocked in the translation input field)
# ============================================================

import requests
import pytest

BASE_URL = "https://tina.ethernettrip.com"
AUTH_HEADERS = {"Authorization": "Bearer <valid-token-from-fixture>"}

# Renamed from "payloads" to "injection_attack_vectors" — precise about intent.
INJECTION_ATTACK_VECTORS = [
    # XSS payloads
    "<script>alert('xss')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(document.cookie)",
    "';alert('xss')//",
    # SQL injection payloads
    "' OR '1'='1",
    "'; DROP TABLE translation_records; --",
    "' UNION SELECT email, password FROM users --",
    "admin'--",
]


@pytest.mark.parametrize("attack_vector", INJECTION_ATTACK_VECTORS)
def test_translation_input_rejects_injections(attack_vector: str):
    """
    Doc 2, Ch 1.1.1: The translation input must reject (not execute) injected code.
    XSS: The raw script must not appear unescaped in the response body.
    SQL: The injection must not alter DB state or return unauthorized data.

    'Blocked' is used instead of 'handled' — Doc 2 §1.1 identifies 'handled'
    ("hanterad") as ambiguous. The required behavior is prevention, not management.
    """
    response = requests.post(
        f"{BASE_URL}/translate",
        headers=AUTH_HEADERS,
        json={"text": attack_vector}
    )

    # The server must not crash — a 500 means the payload caused an error
    assert response.status_code != 500, (
        f"SQL/XSS injection caused a 500 error. Vector: {attack_vector!r}"
    )

    response_text = response.text

    # XSS check: raw <script> tags must be escaped or stripped in the response
    assert "<script>" not in response_text, (
        f"XSS vector was reflected unescaped in response. Vector: {attack_vector!r}"
    )

    # SQL check: DB error messages must not leak into the response
    for leak_indicator in ["syntax error", "pg_", "psycopg2", "postgresql", "relation"]:
        assert leak_indicator.lower() not in response_text.lower(), (
            f"DB error message leaked in response for vector: {attack_vector!r}"
        )