# ============================================================
# Test Category  : Security / Functional
# Requirement(s) : Doc 1 – AC2 (unauthenticated users must be redirected to login)
#                  FR1.2 (login required for translation interface)
# ============================================================

import requests
import pytest

BASE_URL = "https://tina.ethernettrip.com"

PROTECTED_ROUTES = [
    f"{BASE_URL}/",
    f"{BASE_URL}/translate",
    f"{BASE_URL}/history",  # Add any additional protected routes here
]


@pytest.mark.parametrize("route", PROTECTED_ROUTES)
def test_unauthenticated_user_redirected_to_login(route: str):
    """
    AC2: An unauthenticated GET to any protected route must redirect to /login.
    The user must NOT be shown the translation interface without valid session.

    'allow_redirects=False' captures the redirect itself, not the login page.
    """
    response = requests.get(route, allow_redirects=False)

    assert response.status_code in [301, 302], (
        f"Expected redirect for unauthenticated access to {route}, "
        f"got {response.status_code}."
    )

    location = response.headers.get("Location", "")
    assert "login" in location.lower(), (
        f"Redirect does not point to login page. Location: {location}"
    )