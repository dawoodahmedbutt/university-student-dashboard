from sqlalchemy.orm import Session
from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IStudentAssignmentRepo import IStudentAssignmentRepo
from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment as StudentAssignmentTable
from src.Domain_Layer.Entities.StudentAssignment import StudentAssignment as StudentAssignmentEntity

class StudentAssignmentRepo(BaseRepo[StudentAssignmentEntity], IStudentAssignmentRepo):

    def __init__(self, session: Session):
        super().__init__(session, StudentAssignmentTable)

    def get_by_student_and_assignment(self, student_ids: list[int], assignment_ids: list[int]):
        rows = (
            self.session.query(StudentAssignmentTable)
            .filter(StudentAssignmentTable.student_id.in_(student_ids))
            .filter(StudentAssignmentTable.assignment_id.in_(assignment_ids))
            .all()
        )
        return [self._to_entity(r) for r in rows]

    def get_all_by_student(self, student_id: int) -> list[StudentAssignmentEntity]:
        rows = self.session.query(StudentAssignmentTable).filter(StudentAssignmentTable.student_id == student_id).all()
        return [self._to_entity(r) for r in rows]

    def get_all_by_assignment(self, assignment_id: int) -> list[StudentAssignmentEntity]:
        rows = self.session.query(StudentAssignmentTable).filter(StudentAssignmentTable.assignment_id == assignment_id).all()
        return [self._to_entity(r) for r in rows]




    # ORM ↔ Entity conversion helpers

    def _to_entity(self, row: StudentAssignmentTable) -> StudentAssignmentEntity:

        entity = StudentAssignmentEntity(
            student_id=row.student_id,
            assignment_id=row.assignment_id,
            grade=row.grade,
            submitted_date=row.submitted_date
        )
        return entity

    def _to_orm(self, entity: StudentAssignmentEntity) -> StudentAssignmentTable:
        """
        Convert domain entity to ORM row (for add).
        """
        return StudentAssignmentTable(
            student_id=entity.student_id,
            assignment_id=entity.assignment_id,
            grade=entity.grade,
            submission_notes=entity.submission_notes,
        )
