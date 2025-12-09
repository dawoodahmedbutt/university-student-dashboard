from sqlalchemy.orm import Session
from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IModuleRepo import IModuleRepo
from src.Data_Access_Layer.Tables.Module import Module as ModuleTable
from src.Domain_Layer.Entities.Module import Module as ModuleEntity
from src.Domain_Layer.Entities.Course import Course as CourseEntity
from src.Data_Access_Layer.Tables.Course import Course as CourseTable
from src.Data_Access_Layer.Tables.Session import Session as SessionTable
from src.Domain_Layer.Entities.Session import Session as SessionEntity
from src.Data_Access_Layer.Tables.CourseModule import course_modules as CourseModuleTable


class ModuleRepo(BaseRepo[ModuleEntity], IModuleRepo):
    def __init__(self, session: Session):
        super().__init__(session, ModuleTable)
    
    def is_module_in_course(self, module_id: int, course_id: int) -> bool:
        exists = (
        self.session.query(CourseModuleTable)
        .filter(CourseModuleTable.c.course_id == course_id)
        .filter(CourseModuleTable.c.module_id == module_id)
        .first()
    )
        return exists is not None
    

    # ORM ↔ Entity conversion helpers
    def _to_entity(self, orm: ModuleTable) -> ModuleEntity:
        """Convert ORM row to domain entity."""
        entity = ModuleEntity(
            module_id=orm.module_id,
            module_name=orm.module_name,
            credits=orm.credits,
            module_leader=orm.module_leader
        )
        for course in orm.courses:
            entity.add_course(CourseEntity(
                course.course_id,
                course.course_name,
                course.course_director,
                course.education_level
            ))
        return entity
    
    def _to_orm(self, entity):
        orm = ModuleTable(module_id = entity.module_id , module_name =entity.module_name
                           , credits = entity.credits, module_leader = entity.module_leader)
        return orm
    
    def add_module_course(self, module, course_id):
        orm_course = self.session.get(CourseTable, course_id)
        if orm_course is None:
            raise Exception(f"Course with id {course_id} not found.")

        orm_module = self._to_orm(module)
        self.session.add(orm_module)
        self.session.commit()  

        orm_course.modules.append(orm_module)
        self.session.commit()

        return self._to_entity(orm_module)   

    def delete(self, id):
        module = self.session.get(ModuleTable, id)
        if module is None:
            raise Exception(f"module with id = {id} does not exist")
        module.courses.clear()
        self.session.commit()
        return super().delete(id)     