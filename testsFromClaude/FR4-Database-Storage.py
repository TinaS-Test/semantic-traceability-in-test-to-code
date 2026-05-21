# ============================================================
# Test Category  : Integration / Data
# Requirement(s) : Doc 1 – FR4.1 (DB write after translation),
#                  FR4.2 (fields: email, source text, translation, timestamp)
# ============================================================

import psycopg2
import requests
import pytest
from datetime import datetime, timezone

BASE_URL = "https://tina.ethernettrip.com"

# DB connection uses internal VLAN IP only — NFR1.1 and NFR1.3.
DB_CONNECTION_PARAMS = {
    "host":     "192.168.2.3",
    "port":     5432,
    "dbname":   "tina_db",      # Replace with actual DB name
    "user":     "tina_user",    # Replace with actual DB user
    "password": "db_password"   # Must come from environment variable in CI
}

TEST_USER_EMAIL = "qa_test_user@example.com"
SAMPLE_SOURCE_TEXT = "Testmening för databasverifiering"


@pytest.fixture(scope="module")
def db_connection():
    """Opens a direct DB connection for assertion queries."""
    conn = psycopg2.connect(**DB_CONNECTION_PARAMS)
    yield conn
    conn.close()


def test_translation_record_persisted(db_connection):
    """
    FR4.1: After a translation, a record must be written to PostgreSQL.
    FR4.2: The record must contain email, source_text, translation, and timestamp.

    Renamed 'log' to 'translation_record' — a record is retrievable and structured,
    which matches FR4.2's description more precisely than "log".
    """
    # Trigger a translation via the API
    before_timestamp = datetime.now(timezone.utc)

    response = requests.post(
        f"{BASE_URL}/translate",
        headers={"Authorization": "Bearer <valid-token-from-fixture>"},
        json={"text": SAMPLE_SOURCE_TEXT}
    )
    assert response.status_code == 200

    # Query the DB for the most recent translation_record for this user
    cursor = db_connection.cursor()
    cursor.execute(
        """
        SELECT email, source_text, translated_text, created_at
        FROM translation_records
        WHERE email = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (TEST_USER_EMAIL,)
    )
    record = cursor.fetchone()
    cursor.close()

    assert record is not None, "No translation_record found in DB after translation."

    email, source_text, translated_text, created_at = record

    # FR4.2: All four fields must be present and non-empty
    assert email == TEST_USER_EMAIL
    assert source_text == SAMPLE_SOURCE_TEXT
    assert translated_text and len(translated_text) > 0, "translated_text is empty."
    assert created_at >= before_timestamp, (
        "Timestamp in DB predates the request — clock skew or incorrect field."
    )