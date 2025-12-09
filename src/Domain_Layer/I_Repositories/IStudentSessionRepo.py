from abc import ABC, abstractmethod
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.StudentSession import StudentSession as StudentSessionEntity

class IStudentSessionRepo(IBaseRepo[StudentSessionEntity], ABC):

    @abstractmethod
    def get_by_student_and_session(self, student_id: int, session_id: int) -> StudentSessionEntity:
        pass

    @abstractmethod
    def mark_attendance(self, entity: StudentSessionEntity) -> StudentSessionEntity:
        pass

    @abstractmethod
    def get_attendance_for_student(self, student_id: int) -> list[StudentSessionEntity]:
        pass

    @abstractmethod
    def get_attendance_for_session(self, session_id: int) -> list[StudentSessionEntity]:
        pass

    @abstractmethod
    def get_attendance_for(self, student_ids: list[int], session_ids: list[int]):
        pass
