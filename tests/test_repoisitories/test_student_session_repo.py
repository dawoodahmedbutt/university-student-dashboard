from src.Data_Access_Layer.Repositories.StudentsSessionRepo import StudentSessionRepo
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Session import Session
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.StudentSession import StudentSession


def test_studentsessionrepo_get_and_attendance_lists(session):
    course = Course(course_name="CompSci", course_director="Dr. X", education_level="BSc")
    mod = Module(module_name="Prog", credits=20, module_leader="Dr. P")
    session.add_all([course, mod])
    session.commit()

    stud = Student(first_name="Zoe", last_name="Lane", email="zoe@example.com", course=course)
    session.add(stud)
    session.commit()

    s = Session(module_id=mod.module_id, session_location="Room 5", session_date=None, start_time=None, end_time=None)
    session.add(s)
    session.commit()

    ss = StudentSession(student_id=stud.student_id, session_id=s.session_id, status=True)
    session.add(ss)
    session.commit()

    repo = StudentSessionRepo(session)

    got = repo.get_by_student_and_session(stud.student_id, s.session_id)
    assert got is not None
    assert getattr(got, "student_id") == stud.student_id

    # attendance lists
    for_list = repo.get_attendance_for_student(stud.student_id)
    assert isinstance(for_list, list)
    assert len(for_list) >= 1

    for_sess = repo.get_attendance_for_session(s.session_id)
    assert isinstance(for_sess, list)
    assert len(for_sess) >= 1

    # generic filter
    multi = repo.get_attendance_for([stud.student_id], [s.session_id])
    assert isinstance(multi, list)
    assert len(multi) >= 1
