from abc import ABC, abstractmethod
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.Session import Session as EntitySession    

class ISessionRepo(IBaseRepo[EntitySession], ABC):
    
    @abstractmethod
    def get_sessions_by_module(self, module_id: int) -> list[EntitySession]:
        pass