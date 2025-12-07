from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IAssignmentRepo import IAssignmentRepo
from src.Data_Access_Layer.Tables.Assignment import Assignment as AssignmentTable
from src.Domain_Layer.Entities.Assignment import Assignment as AssignmentEntity

class AssignmentRepo(BaseRepo[AssignmentEntity], IAssignmentRepo):

    def __init__(self, session):
        super().__init__(session, AssignmentTable)

    def get_assignments_by_module(self, module_id: int):
        rows = (
            self.session.query(AssignmentTable)
            .filter(AssignmentTable.module_id == module_id)
            .all()
        )
        return [self._to_entity(r) for r in rows]
    
    # ORM ↔ Entity conversion helpers
    def _to_entity(self, row: AssignmentTable) -> AssignmentEntity:
        """Convert ORM row to domain entity."""
        # Domain Assignment expects (assignment_id, module_id, assignment_name, due_date)
        entity = AssignmentEntity(
            row.assignment_id,
            row.module_id,
            row.assignment_name,
            row.due_date,
        )
        return entity    

