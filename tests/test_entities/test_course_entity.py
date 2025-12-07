from src.Domain_Layer.Entities.Course import Course
from src.Domain_Layer.Entities.Module import Module


def test_course_add_module():
    course = Course(1, "CompSci", "Dr X", "BSc")
    mod = Module(module_id=2, module_name="Net", credits=10, module_leader="Dr N")
    course.add_module(mod)
    assert len(course.modules) == 1
    assert course.modules[0] is mod
