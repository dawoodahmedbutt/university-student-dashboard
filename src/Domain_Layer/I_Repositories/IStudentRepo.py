from abc import ABC, abstractmethod
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.Student import Student     

class IStudentRepo(IBaseRepo[Student], ABC):
    
    @abstractmethod
    def get_students_by_course(self, course_id: int):
        pass