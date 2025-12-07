import pytest
from datetime import date, time

from src.Data_Access_Layer.Repositories.SessionRepo import SessionRepo
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Session import Session


def test_sessionrepo_get_by_id_and_list(session):
    mod = Module(module_name="Networks", credits=15, module_leader="Dr. Lee")
    session.add(mod)
    session.commit()

    s = Session(
        module_id=mod.module_id,
        session_location="Room A01",
        session_date=date(2024, 10, 10),
        start_time=time(9, 0),
        end_time=time(11, 0),
    )
    session.add(s)
    session.commit()

    repo = SessionRepo(session)

    # get_by_id should return a domain entity with matching properties
    ent = repo.get_by_id(s.session_id)
    assert ent is not None
    assert getattr(ent, "session_id") == s.session_id
    assert getattr(ent, "session_location") == "Room A01"

    # get_all should include the added session
    all_sessions = repo.get_all()
    assert any(getattr(x, "session_id") == s.session_id for x in all_sessions)


def test_sessionrepo_get_sessions_by_module(session):
    m = Module(module_name="AI", credits=20, module_leader="Prof. Smith")
    session.add(m)
    session.commit()

    s1 = Session(module_id=m.module_id, session_location="Lab 1", session_date=date(2024, 5, 1), start_time=time(14, 0), end_time=time(16, 0))
    s2 = Session(module_id=m.module_id, session_location="Lab 2", session_date=date(2024, 5, 2), start_time=time(10, 0), end_time=time(12, 0))
    session.add_all([s1, s2])
    session.commit()

    repo = SessionRepo(session)
    results = repo.get_sessions_by_module(m.module_id)
    assert isinstance(results, list)
    assert len(results) >= 2
    locs = {getattr(r, "session_location") for r in results}
    assert {"Lab 1", "Lab 2"}.issubset(locs)
