# Test Category:
# Resilience Test

# Requirements Covered:
# AC5

def test_email_failure_does_not_block_translation(
    client,
    mock_email_failure,
    db_session
):
    """
    Ensures failed notifications
    do not interrupt translation flow.

    Semantic focus:
    handled ("hanteras")
    remains stored ("finnas kvar")
    """

    response = client.post("/translate", json={
        "sourceText": "Hej"
    })

    assert response.status_code == 200

    saved_log = db_session.query(TranslationLog).first()

    assert saved_log is not None