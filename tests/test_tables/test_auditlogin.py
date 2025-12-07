import pytest
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from src.Data_Access_Layer.Tables.UserAccount import UserAccount
from src.Data_Access_Layer.Tables.AuditLogin import AuditLogin

# Helper function to generate unique emails
def unique_email():
    return f"user_{datetime.now(timezone.utc).timestamp()}@example.com"

@pytest.fixture
def setup_user(session):
    user = UserAccount(email=unique_email(), password="hashed123", role="staff")
    session.add(user)
    session.commit()
    return user

def test_create_audit_login(session, setup_user):
    user = setup_user
    audit = AuditLogin(user_id=user.user_id, timestamp=datetime.now(timezone.utc))
    session.add(audit)
    session.commit()

    db_audit = session.query(AuditLogin).filter_by(user_id=user.user_id).first()
    assert db_audit is not None
    assert db_audit.user_id == user.user_id
    assert db_audit.timestamp is not None

def test_audit_login_requires_valid_user_fk(session):
    audit = AuditLogin(user_id=9999, timestamp=datetime.now(timezone.utc))
    session.add(audit)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

def test_relationships_linked_correctly(session, setup_user):
    user = setup_user
    audit = AuditLogin(user_id=user.user_id, timestamp=datetime.now(timezone.utc))
    session.add(audit)
    session.commit()

    assert audit.user == user
    assert audit in user.audit_logs

def test_delete_user_cascades_to_audit_log(session, setup_user):
    user = setup_user
    audit = AuditLogin(user_id=user.user_id, timestamp=datetime.now(timezone.utc))
    session.add(audit)
    session.commit()

    session.delete(user)
    session.commit()

    remaining = session.query(AuditLogin).filter_by(user_id=user.user_id).all()
    assert len(remaining) == 0

def test_timestamp_stored_correctly(session, setup_user):
    user = setup_user
    now = datetime.now(timezone.utc)
    audit = AuditLogin(user_id=user.user_id, timestamp=now)
    session.add(audit)
    session.commit()

    db_audit = session.query(AuditLogin).filter_by(user_id=user.user_id).first()
    # ignore tzinfo for SQLite
    assert db_audit.timestamp.replace(tzinfo=None) == now.replace(tzinfo=None)
