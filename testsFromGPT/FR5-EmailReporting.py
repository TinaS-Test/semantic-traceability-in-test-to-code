# Test Category:
# Integration Test

# Requirements Covered:
# FR5.1
# FR5.2

def test_translation_receipt_email_sent(mail_service):
    """
    Verifies receipt generation
    and email dispatch.

    Semantic focus:
    generate ("generera")
    send ("skicka")
    """

    result = mail_service.send_translation_receipt(
        to_email="user@test.com",
        translated_text="Hello"
    )

    assert result.success is True