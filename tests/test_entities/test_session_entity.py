import pytest
from datetime import time, date

from src.Domain_Layer.Entities.Session import Session
from src.Domain_Layer.Entities.Student import Student


def test_session_end_time_must_be_after_start():
    with pytest.raises(ValueError):
        Session(session_id=1, module_id=2, session_location="L", start_time=time(10, 0), end_time=time(9, 0), session_date=date.today())


def test_session_requires_module():
    with pytest.raises(ValueError):
        Session(session_id=1, module_id=None, session_location="L", start_time=time(9, 0), end_time=time(10, 0), session_date=date.today())


def test_add_student_and_duplicate_guard():
    s = Session(session_id=1, module_id=2, session_location="L", start_time=time(9, 0), end_time=time(10, 0), session_date=date.today())
    student = Student(student_id=1, first_name="A", last_name="B", address=None, course_id=1, year_of_study=1, email="a@b.com")
    s.add_student(student)
    assert len(s.students) == 1

    with pytest.raises(ValueError):
        s.add_student(student)
