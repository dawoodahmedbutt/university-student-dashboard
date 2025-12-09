from src.Domain_Layer.Entities.Module import Module
from src.Data_Access_Layer.Repositories.ModuleRepo import ModuleRepo
from src.Exceptions.ModuleExceptions import ModuleException
from datetime import date, time
from sqlalchemy.exc import IntegrityError

class ModuleServices:
    def __init__(self, db):
        self.repo = ModuleRepo(db)

    def getBy_id(self, id: int):
        module = self.repo.get_by_id(id)  # ORM object from Data Access Layer
        return module   

    def get_all(self):
        res = self.repo.get_all()
        return res
    
    def create(self, moduleDTO, course_id):
        module = Module(None,moduleDTO.module_name, moduleDTO.credits, moduleDTO.module_leader)
        try:
            res = self.repo.add_module_course(module, course_id)
            return {"success": True, "module": res}
        except IntegrityError as e:
            # Detect unique constraint failure on module name
            orig = getattr(e, "orig", None)
            msg = str(orig) if orig is not None else str(e)
            if "unique" in msg.lower():
                return {"success": False, "message": f"Module name '{moduleDTO.module_name}' already exists."}
            # Re-raise if it's some other integrity issue
            raise
    
    def update(self, moduleDTO, module_id):
        module = Module(module_id,moduleDTO.module_name, moduleDTO.credits, moduleDTO.module_leader)
        res = self.repo.update(module, module_id)    
        return res
    
    def delete(self, module_id):
        res = self.repo.delete(module_id)        
        return res