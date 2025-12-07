from src.Domain_Layer.Entities.Module import Module
from src.Domain_Layer.Entities.Course import Course
from src.Domain_Layer.Entities.Assignment import Assignment
from src.Domain_Layer.Entities.Session import Session
from datetime import time, date


def test_module_add_course_no_duplicates():
    mod = Module(module_id=1, module_name="M", credits=5, module_leader="L")
    c = Course(1, "C", "D", "BSc")
    mod.add_course(c)
    mod.add_course(c)
    assert len(mod.courses) == 1


def test_module_add_assignment_and_session():
    mod = Module(module_id=1, module_name="M", credits=5, module_leader="L")
    a = Assignment = Assignment = None
   
    assign = Assignment
   
    from src.Domain_Layer.Entities.Assignment import Assignment as AssignmentEntity
    from src.Domain_Layer.Entities.Session import Session as SessionEntity

    ass = AssignmentEntity(1, 1, "A", None)
    sess = SessionEntity(1, 1, "L", time(9, 0), time(10, 0), date.today())
    mod.add_assignment(ass)
    mod.add_session(sess)
    assert mod.assignments[0] is ass
    assert mod.sessions[0] is sess
