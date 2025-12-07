from src.Data_Access_Layer.Repositories.CourseRepo import CourseRepo
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Module import Module


def test_courserepo_get_and_modules(session):
    course = Course(course_name="Maths", course_director="Dr. M", education_level="BSc")
    module = Module(module_name="Algebra", credits=10, module_leader="Dr. A")
    session.add_all([course, module])
    session.commit()

    # associate
    course.modules.append(module)
    session.commit()

    repo = CourseRepo(session)
    ent = repo.get_by_id(course.course_id)
    assert ent is not None
    assert getattr(ent, "course_id") == course.course_id
    assert isinstance(ent.modules, list)
    assert len(ent.modules) >= 1

    all_courses = repo.get_all()
    assert any(getattr(c, "course_id") == course.course_id for c in all_courses)
