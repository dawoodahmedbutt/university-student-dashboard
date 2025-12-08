from src.Data_Access_Layer.Repositories.UserAccountRepo import UserAccountRepo
from src.Data_Access_Layer.Tables.UserAccount import UserAccount
from src.Domain_Layer.Entities.UserAccount import UserAccount as UserAccountEntity


def test_useraccountrepo_get_and_add(session):
    user = UserAccount(email="u@example.com", password="pw", role="admin")
    session.add(user)
    session.commit()

    repo = UserAccountRepo(session)
    ent = repo.get_by_id(user.user_id)
    assert ent is not None
    assert getattr(ent, "email") == "u@example.com"

    # test add via domain entity (uses _to_orm)
    domain = UserAccountEntity(None, "new@example.com", "x", "user")
    added = repo.add(domain)
    assert getattr(added, "email") == "new@example.com"
