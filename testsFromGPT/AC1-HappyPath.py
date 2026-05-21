# Test Category:
# End-to-End Test

# Requirements Covered:
# AC1

def test_complete_translation_cycle(
    client,
    db_session,
    mock_gemini,
    mock_email_service
):
    """
    Verifies complete business flow.

    Semantic focus:
    complete cycle ("fullständig cykel")
    stored ("sparas")
    sent ("skickas")
    """

    mock_gemini.return_value = {
        "translatedText": "Hello world"
    }

    response = client.post("/translate", json={
        "sourceText": "Hej världen"
    })

    assert response.status_code == 200

    saved_log = db_session.query(TranslationLog).first()

    assert saved_log is not None

    assert mock_email_service.was_called is True