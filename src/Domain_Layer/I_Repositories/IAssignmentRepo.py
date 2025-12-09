from abc import ABC,abstractmethod
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.Assignment import Assignment

class IAssignmentRepo(IBaseRepo[Assignment], ABC):
    
    @abstractmethod
    def get_assignments_by_module(self, module_id: int):
        pass
