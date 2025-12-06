import pytest
from sqlalchemy.exc import IntegrityError
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing
from src.Data_Access_Layer.Tables.StudentSession import StudentSession

def test_create_student(session):
    course = Course(course_name="Computer Science", course_director="Dr. Smith", education_level="Undergraduate")
    session.add(course)
    session.commit()

    student = Student(
        first_name="Alice",
        last_name="Johnson",
        email="alice@example.com",
        address="123 Main St",
        year_of_study=2,
        course_id=course.course_id
    )
    session.add(student)
    session.commit()

    db_student = session.query(Student).filter_by(email="alice@example.com").first()
    assert db_student is not None
    assert db_student.first_name == "Alice"
    assert db_student.course.course_name == "Computer Science"

def test_student_email_unique_constraint(session):
    from sqlalchemy.exc import IntegrityError
    course = session.query(Course).first()

    student1 = Student(first_name="Bob", last_name="Smith", email="bob@example.com", course_id=course.course_id)
    session.add(student1)
    session.commit()

    student2 = Student(first_name="Bobby", last_name="Brown", email="bob@example.com", course_id=course.course_id)
    session.add(student2)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_student_requires_course_fk(session):
    student = Student(first_name="Charlie", last_name="Davis", email="charlie@example.com", course_id=9999)
    session.add(student)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
