from src.Domain_Layer.Entities.Assignment import Assignment
from src.Domain_Layer.Entities.Student import Student


def test_assignment_add_student():
    a = Assignment(assignment_id=1, module_id=2, assignment_name="X", due_date=None)
    s = Student(student_id=7, first_name="S", last_name="L", address=None, course_id=1, year_of_study=1, email="s@x.com")
    a.add_student(s)
    assert a.students[0] is s
