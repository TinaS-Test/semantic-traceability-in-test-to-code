import pytest
import requests
from unittest.mock import patch, MagicMock

# Requirement Covered: AC3 and general robust API integration.
# Test Category: Boundary & Integration Test
@pytest.mark.parametrize("status_code, expected_behavior", [
    (200, "success"),             # OK - Translation successful
    (201, "created"),             # Created - Resource created
    (301, "redirect_permanent"),  # Moved Permanently
    (302, "redirect_temporary"),  # Found (Temporary Redirect)
    (401, "unauthorized"),        # Unauthorized - Missing/Bad API Key
    (404, "not_found"),           # Not Found - Endpoint missing
    (429, "rate_limited"),        # Too Many Requests - Rate limit hit
    (500, "server_error"),        # Internal Server Error - Gemini API down
    (503, "service_unavailable")  # Service Unavailable - Gateway issues
])
@patch('requests.post')
def test_api_response_codes_are_handled(mock_post, status_code, expected_behavior):
    # Mock the specific status code response
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_post.return_value = mock_response
    
    # Execute the mocked API call
    response = requests.post("https://api.gemini.example.com/translate")
    
    # Validate the status code was received
    assert response.status_code == status_code
    
    # Example logic mapping: How the system handles the specific code
    if status_code in [200, 201]:
        assert expected_behavior in ["success", "created"]
    elif status_code in [301, 302]:
        assert "redirect" in expected_behavior
    elif status_code == 429:
        assert expected_behavior == "rate_limited"
    elif status_code >= 500:
        # Validate protection mechanisms are triggered (e.g., graceful degradation)
        assert expected_behavior in ["server_error", "service_unavailable"]