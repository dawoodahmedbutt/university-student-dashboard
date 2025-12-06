import pytest
import uuid
from datetime import date
from sqlalchemy.exc import IntegrityError

from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment


# Fixture used to set up module + assignment
@pytest.fixture
def setup_entities(session):
    unique = uuid.uuid4().hex[:6]
    module = Module(module_name=f"AI-{unique}", credits=15, module_leader="Prof X")
    assignment = Assignment(
        module=module,
        assignment_name="Coursework 1",
        due_date=date(2025, 1, 10)
    )

    session.add_all([module, assignment])
    session.commit()
    return module, assignment


def test_create_assignment(session):
    module = Module(module_name="Programming", credits=20, module_leader="Dr. Code")

    assignment = Assignment(
        module=module,
        assignment_name="Lab Report",
        due_date=date(2025, 2, 1)
    )

    session.add_all([module, assignment])
    session.commit()

    db_assignment = session.query(Assignment).filter_by(assignment_name="Lab Report").first()
    assert db_assignment is not None
    assert db_assignment.module_id == module.module_id
    assert db_assignment.due_date == date(2025, 2, 1)


def test_assignment_requires_valid_module_fk(session):
    assignment = Assignment(
        module_id=9999,  # invalid FK
        assignment_name="Ghost Assignment",
        due_date=date(2025, 1, 1)
    )

    session.add(assignment)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_assignment_relationship_with_module(session, setup_entities):
    module, assignment = setup_entities

    assert assignment.module == module
    assert assignment in module.assignments


def test_delete_assignment_deletes_student_assignments(session, setup_entities):
    """
    Requires: Assignment.student_assignments cascade='all, delete-orphan'
    """
    module, assignment = setup_entities

    # Create supporting student + course
    course = Course(course_name="CS", course_director="Dr. Z", education_level="BSc")
    student = Student(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        course=course
    )
    session.add_all([course, student])
    session.commit()

    # Link student to assignment
    sa = StudentAssignment(
        student_id=student.student_id,
        assignment_id=assignment.assignment_id,
        grade=85
    )
    session.add(sa)
    session.commit()

    # Delete assignment
    session.delete(assignment)
    session.commit()

    remaining = session.query(StudentAssignment).filter_by(student_id=student.student_id).all()
    assert len(remaining) == 0


def test_delete_module_deletes_assignments(session):
    """
    Requires: Module.assignments cascade='all, delete-orphan'
    """
    module = Module(module_name="Networks", credits=20, module_leader="Dr. A")
    assignment = Assignment(
        module=module,
        assignment_name="CW2",
        due_date=date(2025, 3, 1)
    )

    session.add_all([module, assignment])
    session.commit()

    session.delete(module)
    session.commit()

    remaining = session.query(Assignment).filter_by(assignment_name="CW2").all()
    assert len(remaining) == 0
