from sqlalchemy.orm import Session
from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IStudentSessionRepo import IStudentSessionRepo
from src.Data_Access_Layer.Tables.StudentSession import StudentSession as StudentSessionTable
from src.Domain_Layer.Entities.StudentSession import StudentSession as StudentSessionEntity
from src.Data_Access_Layer.Tables.Session import Session as SessionTable
from src.Data_Access_Layer.Tables.Student import Student as StudentTable
from src.Data_Access_Layer.Tables.CourseModule import course_modules as CourseModuleTable
from src.Data_Access_Layer.Tables.Module import Module as ModuleTable


class StudentSessionRepo(BaseRepo[StudentSessionEntity], IStudentSessionRepo):
    def __init__(self, session: Session):
        super().__init__(session, StudentSessionTable)

    # Custom methods for attendance
    def get_by_student_and_session(self, student_id: int, session_id: int) -> StudentSessionEntity:
        row = (
            self.session.query(StudentSessionTable)
            .filter(
                StudentSessionTable.student_id == student_id,
                StudentSessionTable.session_id == session_id
            )
            .one_or_none()
        )
        if not row:
            return None
        return self._to_entity(row)

    def mark_attendance(self, entity: StudentSessionEntity) -> StudentSessionEntity:
        record = self.get_by_student_and_session(entity.student_id, entity.session_id)
        
        # Update existing attendance record
        if record:
            orm = self.session.query(StudentSessionTable).get(record.student_session_id)
            orm.status = entity.status
            updated = super().update(orm)
            return self._to_entity(updated)
        return None

    def get_attendance_for_student(self, student_id: int) -> list[StudentSessionEntity]:
        rows = (
            self.session.query(StudentSessionTable)
            .filter(StudentSessionTable.student_id == student_id)
            .all()
        )
        return [self._to_entity(r) for r in rows]

    def get_attendance_for_session(self, session_id: int) -> list[StudentSessionEntity]:
        rows = (
            self.session.query(StudentSessionTable)
            .filter(StudentSessionTable.session_id == session_id)
            .all()
        )
        return [self._to_entity(r) for r in rows]

    def get_attendance_for(self, student_ids: list[int], session_ids: list[int]):
        rows = (
            self.session.query(StudentSessionTable)
            .filter(StudentSessionTable.student_id.in_(student_ids))
            .filter(StudentSessionTable.session_id.in_(session_ids))
            .all()
        )
        return [self._to_entity(r) for r in rows]



    # ORM ↔ Entity conversion helpers
    def _to_entity(self, row: StudentSessionTable) -> StudentSessionEntity:
        """Convert ORM row to domain entity."""
        entity = StudentSessionEntity(
            student_id=row.student_id,
            session_id=row.session_id,
            status=row.status,
        )
        return entity
