import pytest
from datetime import date
from uuid import uuid4

from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing


# Helper factory
def create_student(session):
    student = Student(
        first_name="Test Student",
        last_name = "Jones",
        email=f"test_{uuid4()}@example.com"
    )
    session.add(student)
    session.commit()
    return student


#  SUCCESSFUL CREATION TEST
def test_create_valid_wellbeing_record(session):
    student = create_student(session)

    wellbeing = Wellbeing(
        student_id=student.student_id,
        date=date.today(),
        stress_level=5,
        activity_level=7,
        quality_of_food=8,
        alcohol_drug_consumption=1,
        medication=0,
        hours_slept=8
    )

    session.add(wellbeing)
    session.commit()

    saved = session.query(Wellbeing).first()
    assert saved is not None
    assert saved.stress_level == 5
    assert saved.student.student_id == student.student_id


#  FOREIGN KEY VALIDATION
def test_wellbeing_requires_valid_student_fk(session):
    wellbeing = Wellbeing(
        student_id=99999,  # invalid FK
        date=date.today(),
        stress_level=5,
        activity_level=5,
        quality_of_food=5,
        alcohol_drug_consumption=1,
        medication=1,
        hours_slept=8
    )

    session.add(wellbeing)
    with pytest.raises(Exception):
        session.commit()


#  CHECK CONSTRAINT TESTS
@pytest.mark.parametrize("field, value", [
    ("stress_level", 0),       # invalid (<1)
    ("stress_level", 11),      # invalid (>10)
    ("activity_level", 0),
    ("activity_level", 11),
    ("quality_of_food", 0),
    ("quality_of_food", 11),
    ("alcohol_drug_consumption", -1),
    ("alcohol_drug_consumption", 6),
    ("medication", -1),
    ("medication", 6),
    ("hours_slept", -1),
    ("hours_slept", 25),
])
def test_wellbeing_check_constraints(session, field, value):
    student = create_student(session)

    wellbeing_data = {
        "student_id": student.student_id,
        "date": date.today(),
        "stress_level": 5,
        "activity_level": 5,
        "quality_of_food": 5,
        "alcohol_drug_consumption": 1,
        "medication": 1,
        "hours_slept": 8,
    }

    # Override the invalid field
    wellbeing_data[field] = value

    wellbeing = Wellbeing(**wellbeing_data)
    session.add(wellbeing)

    with pytest.raises(Exception):
        session.commit()


#  RELATIONSHIP TEST
def test_wellbeing_relationship_to_student(session):
    student = create_student(session)

    wellbeing = Wellbeing(
        student_id=student.student_id,
        date=date.today(),
        stress_level=4,
        activity_level=6,
        quality_of_food=7,
        alcohol_drug_consumption=2,
        medication=1,
        hours_slept=7
    )

    session.add(wellbeing)
    session.commit()

    assert wellbeing.student.first_name == student.first_name
    assert wellbeing.student.last_name == student.last_name
    assert wellbeing.student.email == student.email
