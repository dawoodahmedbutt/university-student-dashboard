from datetime import date

from src.Data_Access_Layer.Repositories.AssignmentRepo import AssignmentRepo
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Assignment import Assignment


def test_assignmentrepo_get_by_module(session):
    m = Module(module_name="Databases", credits=10, module_leader="Dr. DB")
    session.add(m)
    session.commit()

    a1 = Assignment(module_id=m.module_id, assignment_name="A1", due_date=None)
    a2 = Assignment(module_id=m.module_id, assignment_name="A2", due_date=None)
    session.add_all([a1, a2])
    session.commit()

    repo = AssignmentRepo(session)
    results = repo.get_assignments_by_module(m.module_id)
    assert isinstance(results, list)
    assert len(results) >= 2
    names = {getattr(r, "assignment_name") for r in results}
    assert {"A1", "A2"}.issubset(names)
