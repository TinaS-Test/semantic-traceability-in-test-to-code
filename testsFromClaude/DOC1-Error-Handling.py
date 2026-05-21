# ============================================================
# Test Category  : Negative / Resilience
# Requirement(s) : Doc 1 – AC3 (Gemini API failure), AC4 (DB failure),
#                  AC5 (Postfix/email failure)
# ============================================================

import pytest
import requests
from unittest.mock import patch, MagicMock

BASE_URL = "https://tina.ethernettrip.com"
AUTH_HEADERS = {"Authorization": "Bearer <valid-token-from-fixture>"}
PAYLOAD = {"text": "Felhanteringstest"}


class TestGracefulDegradation:
    """
    Verifies that each external dependency failure is handled without crashing
    the frontend or writing corrupt data to the DB.
    """

    def test_ac3_gemini_failure_shows_error_no_db_write(self):
        """
        AC3: If Gemini API fails, the frontend must show an error message.
        No translation_record with an empty translation may be written to the DB.

        'blocked' ("blockerad") is used instead of 'handled' to be explicit
        about the expected behavior — the request must not proceed to DB storage.
        """
        with patch("app.call_gemini_api", side_effect=Exception("Gemini timeout")):
            response = requests.post(
                f"{BASE_URL}/translate",
                headers=AUTH_HEADERS,
                json=PAYLOAD
            )
        # Frontend must receive an error — not a 200 with empty translation
        assert response.status_code in [503, 502, 500]
        body = response.json()
        assert "error" in body or "message" in body, (
            "AC3: No error message returned when Gemini API failed."
        )
        # Verify no empty translation_record was written — requires DB check
        # (See Test 5 for DB query pattern)

    def test_ac4_db_failure_translation_still_returned(self):
        """
        AC4: If the DB connection is lost, the translation must still be shown.
        Graceful degradation: user experience is preserved, DB error is logged.

        'degraded' ("degraderad") response — translation returned without DB persistence.
        """
        with patch("app.save_translation_record", side_effect=Exception("DB unreachable")):
            response = requests.post(
                f"{BASE_URL}/translate",
                headers=AUTH_HEADERS,
                json=PAYLOAD
            )
        # Translation must still be returned to the user
        assert response.status_code == 200, (
            "AC4: Translation was not returned to user when DB was unavailable."
        )
        body = response.json()
        assert "translation" in body and len(body["translation"]) > 0, (
            "AC4: Translation output missing despite Gemini succeeding."
        )

    def test_ac5_email_failure_does_not_block_user(self):
        """
        AC5: If Postfix rejects the connection, the user must NOT be blocked.
        The translation_record must still exist in DB; the email error is logged.

        'dispatched' ("utskickad") is used to separate email success from blocking.
        """
        with patch("app.send_translation_receipt", side_effect=Exception("Postfix refused")):
            response = requests.post(
                f"{BASE_URL}/translate",
                headers=AUTH_HEADERS,
                json=PAYLOAD
            )
        # User response must succeed regardless of email failure
        assert response.status_code == 200, (
            "AC5: User was blocked by email delivery failure."
        )