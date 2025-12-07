from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Course import Course


def test_studentrepo_get_students_by_course_and_get_all(session):
    c = Course(course_name="CompSci", course_director="Dr. X", education_level="BSc")
    session.add(c)
    session.commit()

    st = Student(first_name="Tom", last_name="Hill", email="tom@example.com", course=c)
    session.add(st)
    session.commit()

    repo = StudentRepo(session)

    students = repo.get_students_by_course(c.course_id)
    assert isinstance(students, list)
    assert len(students) >= 1
    # ensure returned entity has a first_name attribute matching inserted row
    assert any(getattr(s, "first_name") == "Tom" for s in students)

    all_students = repo.get_all()
    assert any(getattr(s, "first_name") == "Tom" for s in all_students)


def test_studentrepo_get_by_id_and_delete(session):
    c = Course(course_name="History", course_director="Dr. Y", education_level="BA")
    session.add(c)
    session.commit()

    s = Student(first_name="Alice", last_name="Brown", email="alice@example.com", course=c)
    session.add(s)
    session.commit()

    repo = StudentRepo(session)
    ent = repo.get_by_id(s.student_id)
    assert ent is not None

    # delete should remove and return True
    ok = repo.delete(s.student_id)
    assert ok is True
    assert repo.get_by_id(s.student_id) is None
