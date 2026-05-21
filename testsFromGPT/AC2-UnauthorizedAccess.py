# Test Category:
# Security Access Control Test

# Requirements Covered:
# AC2

def test_unauthorized_user_redirected_to_login(client):
    """
    Ensures protected routes deny access.

    Semantic focus:
    deny ("neka")
    redirect ("omdirigera")
    """

    response = client.get("/translate-ui")

    assert response.status_code == 302
    assert "/login" in response.location