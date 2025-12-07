from src.Domain_Layer.Entities.Student import Student
from src.Domain_Layer.Entities.Session import Session
from src.Domain_Layer.Entities.Assignment import Assignment
from datetime import time, date


def test_student_add_session_and_assignment():
    student = Student(student_id=10, first_name="Tom", last_name="Hill", address="X", course_id=1, year_of_study=2, email="t@example.com")
    sess = Session(session_id=1, module_id=2, session_location="R1", start_time=time(9, 0), end_time=time(10, 0), session_date=date.today())
    assign = Assignment(assignment_id=5, module_id=2, assignment_name="A1", due_date=None)

    student.add_session(sess)
    student.add_assignment(assign)

    assert student.sessions[0] is sess
    assert student.assignments[0] is assign
