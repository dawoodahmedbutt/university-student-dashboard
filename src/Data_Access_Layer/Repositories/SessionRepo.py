from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.ISessionRepo import ISessionRepo
from src.Data_Access_Layer.Tables.Session import Session as SessionTable
from src.Domain_Layer.Entities.Session import Session as EntitySession


class SessionRepo(BaseRepo[EntitySession], ISessionRepo):

    def __init__(self, session):
        super().__init__(session, SessionTable)

    # def update(self, entity):
    #     existing = self.get_by_id(entity.id)
    #     if existing is None:
    #         return None

    #     existing.module_id = entity.module_id
    #     existing.start_time =  entity.start_time
    #     existing.end_time = entity.end_time
    #     existing.date = entity.date
    #     return super().update(existing)
    
    def get_sessions_by_module(self, module_id: int) -> list[EntitySession]:
        rows = (
            self.session.query(SessionTable)
            .filter(SessionTable.module_id == module_id)
            .all()
        )
        return [self._to_entity(r) for r in rows]


    
    def _to_entity(self, orm):
        res = EntitySession(session_id=orm.session_id,module_id =  orm.module_id, start_time =  orm.start_time,
                     end_time=  orm.end_time, session_date= orm.session_date, session_location= orm.session_location)
        return res
    
    def _to_orm(self, entity):
        orm = SessionTable(
        module_id=entity.module_id,
        session_date=entity.session_date,
        start_time=entity.start_time,
        end_time=entity.end_time,
        session_location = entity.session_location
    )       
        return orm
