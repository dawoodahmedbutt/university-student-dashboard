from abc import ABC
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.Wellbeing import Wellbeing     

class IWellbeingRepo(IBaseRepo[Wellbeing], ABC):
    pass
