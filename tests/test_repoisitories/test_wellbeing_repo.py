from datetime import date

from src.Data_Access_Layer.Repositories.WellbeingRepo import WellbeingRepo
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing


def test_wellbeingrepo_get_all_and_entity(session):
    course = Course(course_name="Health", course_director="Dr. H", education_level="BSc")
    student = Student(first_name="Nia", last_name="Green", email="nia@example.com", course=course)
    session.add_all([course, student])
    session.commit()

    w = Wellbeing(student_id=student.student_id, date=date(2024, 1, 1), stress_level=5, activity_level=6, quality_of_food=7, alcohol_drug_consumption=1, medication=0, hours_slept=8)
    session.add(w)
    session.commit()

    repo = WellbeingRepo(session)
    allw = repo.get_all()
    assert isinstance(allw, list)
    assert any(getattr(x, "student_id") == student.student_id for x in allw)

    ent = repo.get_by_id(w.wellbeing_id)
    assert ent is not None
    assert getattr(ent, "student_id") == student.student_id
