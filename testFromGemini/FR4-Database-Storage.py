# Test Category:
# Data Persistence / Integration Test

# Requirements Covered:
# FR4.1
# FR4.2

from unittest.mock import patch

@patch('app.database_client.insert')
def test_translation_event_storage(mock_db_insert, client):
    """
    Validates that a complete translation event is securely 
    stored in the database after a successful API call.
    
    Semantic focus:
    store ("lagra")
    event ("händelse")
    log ("logg")
    """
    
    # Simulate an authenticated user posting a translation request
    payload = {"source_text": "Hej världen", "target_language": "en"}
    response = client.post("/translate", json=payload)
    
    # Assert the database insert was called exactly once
    assert mock_db_insert.call_count == 1
    
    # Extract the stored arguments to verify semantic compliance
    stored_data = mock_db_insert.call_args[0][0]
    
    # Assert all required elements of the 'event' are present
    assert "email" in stored_data
    assert "source_text" in stored_data
    assert "translated_text" in stored_data
    assert "timestamp" in stored_data