from src.Domain_Layer.Entities.Session import Session
from src.Data_Access_Layer.Repositories.SessionRepo import SessionRepo
from src.Exceptions.SessionException import SessionException
from src.Exceptions.SessionException import SessionException
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from datetime import date, time

class SessionServices:
    def __init__(self, db):
        self.db = db
        self.repo = SessionRepo(db)

    def create(self, module_id, start_time, end_time, session_date, location):
        
        # module_service = ModuleServices(self.db)
        # if module_service.getBy_id(module_id) is None:
        #     raise SessionException(f"No module has id = {module_id}")
        
        if start_time > end_time:
            raise SessionException("invalid start and end time")
        
        if not isinstance(module_id, int):
            raise SessionException("Invalid module id")
        
        if not isinstance(session_date, date):
            raise SessionException("invalid date form")
        
        if not (isinstance(start_time,time) and isinstance(end_time, time)):
            raise SessionException("invalide time form")

        s = Session(None,module_id,location, start_time,end_time,session_date)
        res = self.repo.add(s)
        return res
    
    def update(self, id, module_id, start_time, end_time, session_date, location):
        if start_time > end_time:
            raise SessionException("invalid start and end time")
        
        s = Session(id,module_id,location,start_time,end_time,session_date)
        res = self.repo.update(s,id)
        if res is None:
            raise SessionException(f"Session with id = {id} is not existed ")

        return res
    
    def delete(self, id):
        if not self.repo.delete(id):
            raise SessionException("Can't find session id")
        return True
    
    def get_id(self, id: int):

        session = self.repo.get_by_id(id)
        if session is None:
            raise SessionException(f"id = {id} not found")
        return session
    
    def get_all(self):
        res = self.repo.get_all()
        return res
