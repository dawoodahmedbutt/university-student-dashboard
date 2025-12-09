from abc import ABC, abstractmethod
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.Module import Module     

class IModuleRepo(IBaseRepo[Module], ABC):
    
    @abstractmethod
    def is_module_in_course(self, module_id: int, course_id: int) -> bool:
        pass

    @abstractmethod
    def add_module_course(self, module, course_id):
        pass