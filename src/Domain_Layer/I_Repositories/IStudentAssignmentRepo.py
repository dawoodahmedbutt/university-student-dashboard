from abc import ABC, abstractmethod
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.StudentAssignment import StudentAssignment

class IStudentAssignmentRepo(IBaseRepo[StudentAssignment], ABC):
    """
    Interface repository for StudentAssignment entity.
    Inherits standard CRUD operations from IBaseRepo.
    Can include custom methods for specific queries like:
    - get_by_student_and_assignment
    - get_all_by_student
    - get_all_by_assignment
    """
    
    @abstractmethod
    def get_by_student_and_assignment(self, student_id: int, assignment_id: int) -> StudentAssignment:
        pass

    @abstractmethod
    def get_all_by_student(self, student_id: int) -> list[StudentAssignment]:
        pass

    @abstractmethod
    def get_all_by_assignment(self, assignment_id: int) -> list[StudentAssignment]:
        pass
