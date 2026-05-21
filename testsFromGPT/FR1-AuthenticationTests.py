# Test Category:
# Security Integration Test

# Requirements Covered:
# FR1.1
# FR1.2
# AC2

def test_login_requires_valid_credentials(client):
    """
    Validates that only authenticated users
    can access the translation interface.

    Semantic focus:
    require ("kräva")
    access ("åtkomst")
    redirect ("omdirigera")
    """

    response = client.post("/login", json={
        "email": "invalid@test.com",
        "password": "wrong-password"
    })

    assert response.status_code == 401
    assert "Invalid credentials" in response.json["message"]