# Test Category:
# Database Integration Test

# Requirements Covered:
# FR4.1
# FR4.2

def test_translation_log_is_persisted(db_session):
    """
    Verifies translation event persistence.

    Semantic focus:
    store ("lagra")
    log ("logg")
    """

    translation = TranslationLog(
        email="user@test.com",
        sourceText="Hej",
        translatedText="Hello"
    )

    db_session.add(translation)
    db_session.commit()

    saved_log = db_session.query(TranslationLog).first()

    assert saved_log.email == "user@test.com"
    assert saved_log.translatedText == "Hello"