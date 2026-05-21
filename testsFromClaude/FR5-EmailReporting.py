# ============================================================
# Test Category  : Unit / Integration
# Requirement(s) : Doc 1 – FR5.1 (generate receipt after translation),
#                  FR5.2 (connect to Postfix and send to user email)
# ============================================================

import pytest
from unittest.mock import patch, MagicMock

POSTFIX_HOST = "46.62.156.134"
POSTFIX_PORT = 25
RECIPIENT_EMAIL = "qa_test_user@example.com"

# Renamed "report" to "translation_receipt" — matches FR5's described purpose:
# a confirmation sent to the user, not an internal system report.


@patch("smtplib.SMTP")
def test_translation_receipt_dispatched(mock_smtp_class):
    """
    FR5.1: A translation_receipt must be generated after a successful translation.
    FR5.2: The receipt must be sent via the Postfix server to the user's email.

    The SMTP connection is mocked to prevent real email delivery during testing.
    """
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    # Import the function under test from the Flask app
    # Replace with actual import path from app.py
    from app import send_translation_receipt  # noqa: F401

    send_translation_receipt(
        recipient_email=RECIPIENT_EMAIL,
        source_text="Hej världen",
        translated_text="Hello world"
    )

    # Assert SMTP connected to the correct Postfix server
    mock_smtp_class.assert_called_once_with(POSTFIX_HOST, POSTFIX_PORT)

    # Assert sendmail was called with the correct recipient
    call_args = mock_smtp_instance.sendmail.call_args
    assert call_args is not None, "sendmail was never called."

    _, recipient, message_body = call_args[0]
    assert recipient == RECIPIENT_EMAIL
    assert len(message_body) > 0, "translation_receipt body is empty."
    assert "Hello world" in message_body, (
        "Translation output not included in receipt body."
    )