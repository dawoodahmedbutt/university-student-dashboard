import pytest
from datetime import date, time
from sqlalchemy.exc import IntegrityError

from src.Data_Access_Layer.Tables.Session import Session
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.StudentSession import StudentSession
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Course import Course


def test_create_session(session):
    module = Module(module_name="Networks", credits=15, module_leader="Dr. Lee")
    session.add(module)
    session.commit()

    new_session = Session(
        module_id=module.module_id,
        session_location="Room A01",
        session_date=date(2024, 10, 10),
        start_time=time(9, 0),
        end_time=time(11, 0)
    )
    session.add(new_session)
    session.commit()

    db_session = session.query(Session).first()
    assert db_session is not None
    assert db_session.session_location == "Room A01"
    assert db_session.start_time == time(9, 0)
    assert db_session.end_time == time(11, 0)


def test_session_requires_valid_module_fk(session):
    """
    NOTE: With SQLite, FK constraints require PRAGMA foreign_keys=ON.
    Your test setup must include this in engine creation.
    """
    bad_session = Session(
        module_id=9999,
        session_location="Room X",
        session_date=date(2024, 1, 1),
        start_time=time(10, 0),
        end_time=time(11, 0)
    )
    session.add(bad_session)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_session_relationship_with_module(session):
    module = Module(module_name="AI", credits=20, module_leader="Prof. Smith")
    session.add(module)
    session.commit()

    s = Session(
        module_id=module.module_id,
        session_location="Lab 4",
        session_date=date(2024, 5, 1),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    session.add(s)
    session.commit()

    db_module = session.query(Module).filter_by(module_name="AI").first()
    assert len(db_module.sessions) == 1
    assert db_module.sessions[0].session_location == "Lab 4"




def test_session_cascades_delete_student_sessions(session):
    # Create module + session
    module = Module(module_name="Programming", credits=20, module_leader="Dr. Code")
    session.add(module)
    session.commit()

    s = Session(
        module_id=module.module_id,
        session_location="Room 101",
        session_date=date(2024, 6, 1),
        start_time=time(9, 0),
        end_time=time(11, 0),
    )
    session.add(s)
    session.commit()

    # Create course + student
    course = Course(course_name="CompSci", course_director="Dr. X", education_level="BSc")
    student = Student(first_name="Tom", last_name="Hill", email="tom@example.com", course=course)
    session.add(course)
    session.add(student)
    session.commit()

    ss = StudentSession(student_id=student.student_id, session_id=s.session_id, status=1)
    session.add(ss)
    session.commit()

    # Delete Session so student_session should be orphan-deleted
    session.delete(s)
    session.commit()

    remaining = session.query(StudentSession).all()
    assert remaining == []
