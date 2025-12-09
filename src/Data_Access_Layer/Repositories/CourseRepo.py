from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.ICourseRepo import ICourseRepo
from src.Data_Access_Layer.Tables.Course import Course as CourseTable
from src.Domain_Layer.Entities.Course import Course as CourseEntity

class CourseRepo(BaseRepo[CourseEntity], ICourseRepo):

    def __init__(self, session):
        super().__init__(session, CourseTable)       

    def _to_entity(self, orm):
        res = CourseEntity(course_id=orm.course_id ,course_name=orm.course_name ,
                           course_director=orm.course_director ,education_level=orm.education_level)
        res.modules = list(orm.modules)
        return res
    
    def _to_orm(self, entity):
        res = CourseTable(course_id= entity.course_id,course_name=entity.course_name,
                        course_director= entity.course_director,education_level=entity.education_level)
        return res

    
