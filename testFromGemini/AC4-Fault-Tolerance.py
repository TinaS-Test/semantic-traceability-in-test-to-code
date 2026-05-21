# Test Category:
# Error Handling / Edge Case Test

# Requirements Covered:
# AC4

import logging
from unittest.mock import patch

@patch('app.database_client.insert')
@patch('app.gemini_api.translate')
def test_translation_succeeds_when_db_fails(mock_translate, mock_db_insert, client, caplog):
    """
    Validates that the translation is still returned to the 
    user even if the database connection drops, while ensuring
    the error is internally handled and logged.
    
    Semantic focus:
    handle ("hantera")
    crash ("krascha")
    log ("logga")
    """
    
    # Mock successful translation but a database timeout/failure
    mock_translate.return_value = "Hello world"
    mock_db_insert.side_effect = ConnectionError("PostgreSQL unreachable")
    
    with caplog.at_level(logging.ERROR):
        payload = {"source_text": "Hej världen", "target_language": "en"}
        response = client.post("/translate", json=payload)
        
        # Validate graceful degradation: The translation still succeeds for the user
        assert response.status_code == 200
        assert response.json["translation"] == "Hello world"
        
        # Validate the error was handled and logged internally, preventing a crash
        assert "PostgreSQL unreachable" in caplog.text