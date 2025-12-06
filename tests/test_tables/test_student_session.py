import pytest
import uuid
from datetime import date, time
from sqlalchemy.exc import IntegrityError

from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Session import Session
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.StudentSession import StudentSession


# Helper function to create UNIQUE sample course, module, session, student
@pytest.fixture
def setup_entities(session):
    unique = uuid.uuid4().hex[:6]

    course = Course(
        course_name=f"CS-{unique}", 
        course_director="Dr. X", 
        education_level="BSc"
    )

    module = Module(
        module_name=f"AI-{unique}",
        credits=20,
        module_leader="Prof Y"
    )

    sess = Session(
        module=module,
        session_location="Room 101",
        session_date=date(2025, 1, 1),
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    student = Student(
        first_name="John",
        last_name="Doe",
        email=f"john-{unique}@example.com",
        course=course
    )

    session.add_all([course, module, sess, student])
    session.commit()
    return student, sess


def test_create_student_session(session, setup_entities):
    student, sess = setup_entities

    ss = StudentSession(student_id=student.student_id, session_id=sess.session_id, status=True)
    session.add(ss)
    session.commit()

    db_ss = session.query(StudentSession).filter_by(student_id=student.student_id).first()
    assert db_ss is not None
    assert db_ss.status is True
    assert db_ss.session_id == sess.session_id
    assert db_ss.student_id == student.student_id


def test_unique_constraint_student_session(session, setup_entities):
    student, sess = setup_entities

    ss1 = StudentSession(student_id=student.student_id, session_id=sess.session_id, status=True)
    session.add(ss1)
    session.commit()

    ss2 = StudentSession(student_id=student.student_id, session_id=sess.session_id, status=False)
    session.add(ss2)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_student_session_requires_valid_student_fk(session, setup_entities):
    student, sess = setup_entities

    invalid_student = StudentSession(student_id=9999, session_id=sess.session_id, status=True)
    session.add(invalid_student)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_student_session_requires_valid_session_fk(session, setup_entities):
    student, sess = setup_entities

    invalid_session = StudentSession(student_id=student.student_id, session_id=9999, status=True)
    session.add(invalid_session)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_relationships_linked_correctly(session, setup_entities):
    student, sess = setup_entities

    ss = StudentSession(student_id=student.student_id, session_id=sess.session_id, status=True)
    session.add(ss)
    session.commit()

    assert ss.student == student
    assert ss.session == sess
    assert ss in student.student_sessions
    assert ss in sess.student_sessions


def test_delete_session_cascades_to_student_session(session, setup_entities):
    """
    Only passes if Session.student_sessions has cascade='all, delete-orphan'
    """
    student, sess = setup_entities

    ss = StudentSession(student_id=student.student_id, session_id=sess.session_id, status=True)
    session.add(ss)
    session.commit()

    session.delete(sess)
    session.commit()

    remaining = session.query(StudentSession).filter_by(student_id=student.student_id).all()
    assert len(remaining) == 0


def test_delete_student_cascades_to_student_session(session, setup_entities):
    """
    Only passes if Student.student_sessions has cascade='all, delete-orphan'
    """
    student, sess = setup_entities

    ss = StudentSession(student_id=student.student_id, session_id=sess.session_id, status=True)
    session.add(ss)
    session.commit()

    session.delete(student)
    session.commit()

    remaining = session.query(StudentSession).filter_by(session_id=sess.session_id).all()
    assert len(remaining) == 0
