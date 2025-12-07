from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.ICourseRepo import ICourseRepo
from src.Data_Access_Layer.Tables.Course import Course as CourseTable
from src.Domain_Layer.Entities.Course import Course as CourseEntity

class CourseRepo(BaseRepo[CourseEntity], ICourseRepo):

    def __init__(self, session):
        super().__init__(session, CourseTable)       

    def _to_entity(self, orm):
        # Map ORM fields to domain entity constructor parameters
        res = CourseEntity(
            orm.course_id,
            orm.course_name,
            orm.course_director,
            orm.education_level,
        )
        # keep associated modules as list of ORM Module objects (domain modules can be added separately)
        res.modules = list(orm.modules)
        return res
    
    def _to_orm(self, entity):
        # Create ORM Course from domain entity attributes
        return CourseTable(
            course_id=getattr(entity, "course_id", None),
            course_name=getattr(entity, "course_name", getattr(entity, "name", None)),
            course_director=getattr(entity, "course_director", getattr(entity, "director", None)),
            education_level=getattr(entity, "education_level", None),
        )

    
