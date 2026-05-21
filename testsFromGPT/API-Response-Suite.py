# Test Category:
# API Contract Test

def test_translate_returns_200(client):
    response = client.post("/translate")
    assert response.status_code == 200


def test_login_returns_401_for_invalid_user(client):
    response = client.post("/login")
    assert response.status_code == 401


def test_unknown_route_returns_404(client):
    response = client.get("/unknown-route")
    assert response.status_code == 404


def test_gemini_timeout_returns_503(client):
    response = client.post("/translate")
    assert response.status_code == 503