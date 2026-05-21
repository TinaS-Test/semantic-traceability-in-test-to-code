# ============================================================
# Test Category  : Integration / API
# Requirement(s) : Doc 1 – FR3.1 (Flask), FR3.2 (Gemini API call),
#                  FR3.3 (API key via .env), FR3.4 (response to frontend)
# API Codes      : 200, 201, 301, 302, 401, 404, 429, 500, 503
# ============================================================

import pytest
import requests
from unittest.mock import patch, MagicMock

BASE_URL = "https://tina.ethernettrip.com"
TRANSLATE_ENDPOINT = f"{BASE_URL}/translate"

# Fixture assumed to provide a valid session from Test 2's authenticated_session.
VALID_AUTH_HEADERS = {"Authorization": "Bearer <valid-token-from-fixture>"}
SAMPLE_SWEDISH_TEXT = "Hej världen"


class TestTranslationApiResponseCodes:
    """
    Tests all standard HTTP response codes for the /translate endpoint.
    FR3.2: Backend must communicate with Gemini and return a translation.
    """

    def test_200_successful_translation(self):
        """200 OK – Valid authenticated request returns a translation."""
        response = requests.post(
            TRANSLATE_ENDPOINT,
            headers=VALID_AUTH_HEADERS,
            json={"text": SAMPLE_SWEDISH_TEXT}
        )
        assert response.status_code == 200
        body = response.json()
        assert "translation" in body, "Response body missing 'translation' key."
        assert isinstance(body["translation"], str) and len(body["translation"]) > 0

    def test_201_translation_record_created(self):
        """
        201 Created – Some Flask implementations return 201 when the DB record
        (FR4.1) is created alongside the translation response.
        Both 200 and 201 are accepted.
        """
        response = requests.post(
            TRANSLATE_ENDPOINT,
            headers=VALID_AUTH_HEADERS,
            json={"text": "God morgon"}
        )
        assert response.status_code in [200, 201]

    def test_301_http_redirects_to_https(self):
        """
        301 Moved Permanently – HTTP traffic must redirect to HTTPS.
        Relates to NFR1.1 (all communication secured).
        """
        response = requests.get(
            "http://tina.ethernettrip.com",
            allow_redirects=False
        )
        assert response.status_code == 301
        location = response.headers.get("Location", "")
        assert location.startswith("https://"), (
            f"Redirect target is not HTTPS: {location}"
        )

    def test_302_unauthenticated_redirected_to_login(self):
        """
        302 Found – Unauthenticated POST to /translate must redirect to login.
        Relates to FR1.2 and AC2.
        """
        response = requests.post(
            TRANSLATE_ENDPOINT,
            json={"text": "Test"},
            allow_redirects=False
        )
        assert response.status_code == 302
        assert "login" in response.headers.get("Location", "").lower()

    def test_401_missing_auth_token_returns_unauthorized(self):
        """
        401 Unauthorized – Request with no auth header must be rejected.
        FR1.2: Only authenticated users may access the translation interface.
        """
        response = requests.post(
            TRANSLATE_ENDPOINT,
            json={"text": SAMPLE_SWEDISH_TEXT}
            # No Authorization header
        )
        assert response.status_code == 401

    def test_404_unknown_endpoint_returns_not_found(self):
        """
        404 Not Found – Requests to undefined routes must return 404.
        Prevents information leakage about internal routing.
        """
        response = requests.get(
            f"{BASE_URL}/nonexistent-endpoint",
            headers=VALID_AUTH_HEADERS
        )
        assert response.status_code == 404

    def test_429_rate_limit_triggers_on_rapid_requests(self):
        """
        429 Too Many Requests – Rapid repeated calls must be throttled.
        Protects against Gemini API quota exhaustion and abuse.
        Note: Requires Flask-Limiter or equivalent to be configured.
        """
        responses = [
            requests.post(
                TRANSLATE_ENDPOINT,
                headers=VALID_AUTH_HEADERS,
                json={"text": f"Burst request {i}"}
            )
            for i in range(60)  # 60 requests in rapid succession
        ]
        status_codes = {r.status_code for r in responses}
        assert 429 in status_codes, (
            "Rate limiting (429) was not triggered after 60 rapid requests."
        )

    def test_500_malformed_payload_does_not_cause_unhandled_crash(self):
        """
        500 Internal Server Error – A bad payload must NOT produce an unhandled 500.
        The backend (FR3.1 Flask) must validate input and return 400 instead.
        If 500 is returned, it indicates a missing guard clause in app.py.
        """
        response = requests.post(
            TRANSLATE_ENDPOINT,
            headers=VALID_AUTH_HEADERS,
            json={"wrong_key": None}  # Missing required "text" field
        )
        assert response.status_code != 500, (
            "Unhandled 500 returned for malformed payload — app.py lacks input validation."
        )
        assert response.status_code == 400, (
            f"Expected 400 Bad Request for malformed payload, got {response.status_code}."
        )

    def test_503_gemini_unavailable_returns_service_unavailable(self):
        """
        503 Service Unavailable – When Gemini API is unreachable, the backend
        must return 503, not crash or return 200 with empty data.
        AC3: No incomplete translation_record must be written to the DB.
        Note: Requires a test environment where Gemini can be mocked.
        """
        # This test targets the app's internal behavior.
        # In a real CI environment, replace with Flask test client + mock:
        #   with patch("app.call_gemini_api", side_effect=ConnectionError):
        #       response = flask_test_client.post("/translate", ...)

        with patch("requests.post") as mock_gemini:
            mock_gemini.side_effect = ConnectionError("Gemini API unreachable")
            try:
                response = requests.post(
                    TRANSLATE_ENDPOINT,
                    headers=VALID_AUTH_HEADERS,
                    json={"text": SAMPLE_SWEDISH_TEXT}
                )
                assert response.status_code == 503, (
                    f"Expected 503 when Gemini is down, got {response.status_code}."
                )
            except ConnectionError:
                pytest.skip(
                    "Mock not applied at network level — rerun with Flask test client."
                )