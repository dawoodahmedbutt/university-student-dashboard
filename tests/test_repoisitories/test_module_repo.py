from src.Data_Access_Layer.Repositories.ModuleRepo import ModuleRepo
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Course import Course


def test_modulerepo_is_module_in_course(session):
    course = Course(course_name="CompSci", course_director="Dr. A", education_level="BSc")
    module = Module(module_name="Databases", credits=10, module_leader="Dr. DB")
    session.add_all([course, module])
    session.commit()

    # associate module with course via relationship
    course.modules.append(module)
    session.commit()

    repo = ModuleRepo(session)
    assert repo.is_module_in_course(module.module_id, course.course_id) is True

    # non-existent combination should be False
    assert repo.is_module_in_course(9999, course.course_id) is False
