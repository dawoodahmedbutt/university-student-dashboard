import pytest
import uuid
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError

from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Course import Course


# Helper fixture to create Student + Assignment
@pytest.fixture
def setup_entities(session):
    # Create course + student
    unique = uuid.uuid4().hex[:6]
    course = Course(course_name=f"CS-{unique}", course_director="Dr. X", education_level="BSc")
    student = Student(
        first_name="John",
        last_name="Doe",
        email=f"john{unique}@example.com",
        course=course,
    )

    # Create module + assignment
    module = Module(module_name=f"Datascience-{unique}", credits=15, module_leader="Prof Y")
    assignment = Assignment(
        module=module,
        assignment_name="Coursework 1",
        due_date=date(2025, 1, 15)
    )

    session.add_all([course, student, module, assignment])
    session.commit()
    return student, assignment


# Creation
def test_create_student_assignment(session, setup_entities):
    student, assignment = setup_entities

    sa = StudentAssignment(
        student_id=student.student_id,
        assignment_id=assignment.assignment_id,
        submitted_date=datetime(2025, 1, 10, 12, 0),
        grade=85.5,
    )

    session.add(sa)
    session.commit()

    db_sa = session.query(StudentAssignment).filter_by(student_id=student.student_id).first()
    assert db_sa is not None
    assert db_sa.assignment_id == assignment.assignment_id
    assert db_sa.grade == 85.5
    assert db_sa.submitted_date.year == 2025


# Unique constraint
def test_unique_constraint_student_assignment(session, setup_entities):
    student, assignment = setup_entities

    sa1 = StudentAssignment(
        student_id=student.student_id,
        assignment_id=assignment.assignment_id,
        grade=90,
    )
    session.add(sa1)
    session.commit()

    sa2 = StudentAssignment(
        student_id=student.student_id,
        assignment_id=assignment.assignment_id,
        grade=70,
    )
    session.add(sa2)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


# FK validation
def test_student_assignment_requires_valid_student_fk(session, setup_entities):
    student, assignment = setup_entities

    invalid = StudentAssignment(
        student_id=9999,  
        assignment_id=assignment.assignment_id,
        grade=70,
    )

    session.add(invalid)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_student_assignment_requires_valid_assignment_fk(session, setup_entities):
    student, assignment = setup_entities

    invalid = StudentAssignment(
        student_id=student.student_id,
        assignment_id=9999,  
        grade=70,
    )

    session.add(invalid)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


# Relationship checks
def test_relationships_linked_correctly(session, setup_entities):
    student, assignment = setup_entities

    sa = StudentAssignment(
        student_id=student.student_id,
        assignment_id=assignment.assignment_id,
        grade=88,
    )
    session.add(sa)
    session.commit()

    assert sa.student == student
    assert sa.assignment == assignment
    assert sa in student.student_assignments
    assert sa in assignment.student_assignments



def test_delete_student_deletes_student_assignment(session, setup_entities):
    student, assignment = setup_entities

    sa = StudentAssignment(
        student_id=student.student_id,
        assignment_id=assignment.assignment_id,
        grade=55,
    )
    session.add(sa)
    session.commit()

    session.delete(student)
    session.commit()

    remaining = session.query(StudentAssignment).filter_by(assignment_id=assignment.assignment_id).all()
    assert len(remaining) == 0


