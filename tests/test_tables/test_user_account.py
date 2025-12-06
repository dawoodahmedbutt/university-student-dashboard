import pytest
from uuid import uuid4

from src.Data_Access_Layer.Tables.UserAccount import UserAccount
from src.Data_Access_Layer.Tables.AuditLogin import AuditLogin


# Helper to generate unique emails
def unique_email():
    return f"user_{uuid4()}@example.com"


# SUCCESSFUL CREATION
def test_create_user_account(session):
    user = UserAccount(
        email=unique_email(),
        password="hashedpassword123",
        role="admin"
    )

    session.add(user)
    session.commit()

    saved = session.query(UserAccount).first()
    assert saved is not None
    assert saved.email.startswith("user_")
    assert saved.role == "admin"


# UNIQUE EMAIL CONSTRAINT
def test_unique_email_constraint(session):
    email = unique_email()

    user1 = UserAccount(email=email, password="pw1", role="staff")
    session.add(user1)
    session.commit()

    user2 = UserAccount(email=email, password="pw2", role="staff")
    session.add(user2)

    with pytest.raises(Exception):
        session.commit()

