# Test Category:
# API Integration Test

# Requirements Covered:
# FR3.2
# FR3.4

def test_backend_returns_translated_text(client, mock_gemini):
    """
    Ensures backend forwards request
    and returns translated response.

    Semantic focus:
    send ("skicka")
    return ("returnera")
    """

    mock_gemini.return_value = {
        "translatedText": "Hello world"
    }

    response = client.post("/translate", json={
        "sourceText": "Hej världen"
    })

    assert response.status_code == 200
    assert response.json["translatedText"] == "Hello world"