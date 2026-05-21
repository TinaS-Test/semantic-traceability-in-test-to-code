# Test Category:
# Fault Tolerance Test

# Requirements Covered:
# AC3

def test_no_partial_log_saved_when_gemini_fails(
    client,
    db_session,
    mock_gemini_failure
):
    """
    Ensures failed translations
    are not persisted.

    Semantic focus:
    unavailable ("otillgänglig")
    incomplete data ("ofullständig data")
    """

    response = client.post("/translate", json={
        "sourceText": "Hej"
    })

    assert response.status_code == 503

    saved_logs = db_session.query(TranslationLog).all()

    assert len(saved_logs) == 0