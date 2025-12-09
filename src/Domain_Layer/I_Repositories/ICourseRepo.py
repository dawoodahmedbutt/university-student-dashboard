from abc import ABC
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.Course import Course     

class ICourseRepo(IBaseRepo[Course], ABC):
    pass
