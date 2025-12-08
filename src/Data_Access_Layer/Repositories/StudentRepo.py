from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IStudentRepo import IStudentRepo
from src.Data_Access_Layer.Tables.Student import Student as StudentTable
from src.Domain_Layer.Entities.Student import Student as StudentEntity
class StudentRepo(BaseRepo[StudentEntity], IStudentRepo):

    def __init__(self, session):
        super().__init__(session, StudentTable)

    def add(self, orm):
        
        return super().add(orm)
    
    def _to_entity(self, row: StudentTable) -> StudentEntity:
        """Convert ORM row to domain entity."""
        entity = StudentEntity(
            student_id=row.student_id,
            first_name=row.first_name,
            last_name=row.last_name,
            address=row.address,
            course_id=row.course_id,
            year_of_study=row.year_of_study,
            email=row.email,
        )
        return entity
    
    def get_students_by_course(self, course_id: int):
        rows = (
            self.session.query(StudentTable)
            .filter(StudentTable.course_id == course_id)
            .all()
        )
        return [self._to_entity(r) for r in rows]

    
    # def _to_orm(self, entity):
    #     orm = StudentTable(student_id= entity.)
    #     return 