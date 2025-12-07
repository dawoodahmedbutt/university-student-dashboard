from datetime import datetime, timezone

from src.Data_Access_Layer.Repositories.AuditLogRepo import AuditLogRepo
from src.Data_Access_Layer.Repositories.UserAccountRepo import UserAccountRepo
from src.Data_Access_Layer.Tables.UserAccount import UserAccount
from src.Domain_Layer.Entities.AuditLog import AuditLog as AuditLogEntity


def test_auditlogrepo_add_and_get(session):
    # create user
    user = UserAccount(email="loguser@example.com", password="pw", role="user")
    session.add(user)
    session.commit()

    repo = AuditLogRepo(session)

    # create domain audit entity and add via repo
    now = datetime.now(timezone.utc)
    domain = AuditLogEntity(None, user.user_id, now)
    added = repo.add(domain)
    assert getattr(added, "user_id") == user.user_id

    fetched = repo.get_by_id(added.log_id)
    assert fetched is not None
    assert getattr(fetched, "user_id") == user.user_id
