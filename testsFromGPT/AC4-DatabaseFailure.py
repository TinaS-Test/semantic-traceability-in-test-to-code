# Test Category:
# Resilience Test

# Requirements Covered:
# AC4

def test_translation_visible_during_database_failure(
    client,
    mock_database_failure,
    mock_gemini
):
    """
    Ensures user experience continues
    despite database outage.

    Semantic focus:
    graceful degradation
    without crashing ("utan att krascha")
    """

    mock_gemini.return_value = {
        "translatedText": "Hello"
    }

    response = client.post("/translate", json={
        "sourceText": "Hej"
    })

    assert response.status_code == 200
    assert response.json["translatedText"] == "Hello"