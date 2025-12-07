from src.Domain_Layer.Entities.UserAccount import UserAccount


def test_useraccount_add_log():
    ua = UserAccount(user_id=1, email="a@b.com", password="pw", role="admin")
    assert ua.logs == []
    ua.add_log({"event": "login"})
    assert len(ua.logs) == 1
    assert ua.logs[0]["event"] == "login"
