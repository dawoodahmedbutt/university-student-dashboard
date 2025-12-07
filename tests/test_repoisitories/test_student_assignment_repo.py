from src.Data_Access_Layer.Repositories.StudentAssignmentRepo import StudentAssignmentRepo
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment


def test_studentassignmentrepo_queries(session):
    course = Course(course_name="CompSci", course_director="Dr. X", education_level="BSc")
    mod = Module(module_name="Prog", credits=20, module_leader="Dr. P")
    session.add_all([course, mod])
    session.commit()

    stud = Student(first_name="Zoe", last_name="Lane", email="zoe@example.com", course=course)
    session.add(stud)
    session.commit()

    assign = Assignment(module_id=mod.module_id, assignment_name="Proj", due_date=None)
    session.add(assign)
    session.commit()

    sa = StudentAssignment(student_id=stud.student_id, assignment_id=assign.assignment_id, grade=88.0, submitted_date=None)
    session.add(sa)
    session.commit()

    repo = StudentAssignmentRepo(session)

    by_pair = repo.get_by_student_and_assignment([stud.student_id], [assign.assignment_id])
    assert isinstance(by_pair, list)
    assert len(by_pair) >= 1

    by_student = repo.get_all_by_student(stud.student_id)
    assert isinstance(by_student, list)
    assert len(by_student) >= 1

    by_assignment = repo.get_all_by_assignment(assign.assignment_id)
    assert isinstance(by_assignment, list)
    assert len(by_assignment) >= 1
