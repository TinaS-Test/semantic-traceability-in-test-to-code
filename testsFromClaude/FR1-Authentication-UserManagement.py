# ============================================================
# Test Category  : Integration / Functional
# Requirement(s) : Doc 1 – FR1.1 (registration), FR1.2 (login), FR1.3 (password encryption)
# ============================================================

import requests
import pytest

BASE_URL = "https://tina.ethernettrip.com"

# Renamed from "test_user" to "registered_user_credentials" — explicit intent.
REGISTERED_USER_CREDENTIALS = {
    "email": "qa_test_user@example.com",
    "password": "QaSecure!2024"
}


@pytest.fixture(scope="module")
def authenticated_session() -> requests.Session:
    """
    Fixture: registers a test user and returns an authenticated session.
    Reused by other tests that require authentication.
    """
    session = requests.Session()

    # FR1.1 – Register account
    register_response = session.post(
        f"{BASE_URL}/register",
        json=REGISTERED_USER_CREDENTIALS
    )
    assert register_response.status_code in [200, 201], (
        f"Registration failed: {register_response.status_code}"
    )

    # FR1.3 – Password must not appear in any registration response
    assert REGISTERED_USER_CREDENTIALS["password"] not in register_response.text, (
        "SECURITY VIOLATION: Plain-text password found in registration response."
    )

    # FR1.2 – Login with valid credentials
    login_response = session.post(
        f"{BASE_URL}/login",
        json=REGISTERED_USER_CREDENTIALS
    )
    assert login_response.status_code == 200, (
        f"Login failed with valid credentials: {login_response.status_code}"
    )

    # Confirm session token or cookie is present
    has_session = (
        "token" in login_response.json()
        or session.cookies.get("session") is not None
    )
    assert has_session, "No session token or cookie returned after login."

    return session


def test_user_registration_and_login(authenticated_session):
    """
    Confirms that the authenticated_session fixture succeeds end-to-end.
    Covers FR1.1, FR1.2, and FR1.3.
    """
    assert authenticated_session is not None