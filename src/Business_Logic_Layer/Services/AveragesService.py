from collections import defaultdict
from typing import List, Dict
from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo
from src.Data_Access_Layer.Repositories.StudentsSessionRepo import StudentSessionRepo
from src.Data_Access_Layer.Repositories.StudentAssignmentRepo import StudentAssignmentRepo
from src.Data_Access_Layer.Repositories.SessionRepo import SessionRepo
from src.Data_Access_Layer.Repositories.AssignmentRepo import AssignmentRepo
from src.Data_Access_Layer.Repositories.ModuleRepo import ModuleRepo
from src.Domain_Layer.Entities.Module import Module as ModuleEntity
from src.Business_Logic_layer.Services.BarplotService import BarPlotService

class AveragesService:
    def __init__(self, session):
        # Initialize the repositories with the same DB session
        self.student_repo = StudentRepo(session)
        self.student_session_repo = StudentSessionRepo(session)
        self.student_assignment_repo = StudentAssignmentRepo(session)
        self.session_repo = SessionRepo(session)
        self.assignment_repo = AssignmentRepo(session)
        self.module_repo = ModuleRepo(session)

    def get_modules_for_course(self, course_id: int) -> List[ModuleEntity]:
        """Fetch all modules for a given course."""
        all_modules = self.module_repo.get_all()
        return [m for m in all_modules if any(c.course_id == course_id for c in m.courses)]
    
    def calculate_attendance_percentage(self, module_id: int,course_id) -> float:
        """Calculate average attendance % for a module."""
        student_sessions = self.get_attendance_report_for_module(module_id, course_id)
        if not student_sessions:
            return 0.0
        
        total_sessions = len(student_sessions)
        present_count = sum(1 for s in student_sessions if s.status == True)
        
        return (present_count / total_sessions) * 100 if total_sessions > 0 else 0.0
    
    def get_modules_for_course(self, course_id: int) -> List[ModuleEntity]:
        """Fetch all modules for a given course."""
        all_modules = self.module_repo.get_all()
        return [m for m in all_modules if any(c.course_id == course_id for c in m.courses)]
    
    def get_attendance_report_for_module(self, module_id: int, course_id: int):
        # verifying module belongs to course
        if not self.module_repo.is_module_in_course(module_id, course_id):
            raise ValueError("Module does not belong to course")

        # getting students enrolled in the course
        students = self.student_repo.get_students_by_course(course_id)

        # getting sessions of this module
        sessions = self.session_repo.get_sessions_by_module(module_id)

        # extracting ids
        student_ids = [s.student_id for s in students]
        session_ids = [s.session_id for s in sessions]
        
        # fetching attendance records
        attendance_report = self.student_session_repo.get_attendance_for(student_ids, session_ids)

        return attendance_report   
    

    def get_performance_report_for_module(self, module_id: int, course_id: int):
        if not self.module_repo.is_module_in_course(module_id, course_id):
            raise ValueError("Module does not belong to course")

        students = self.student_repo.get_students_by_course(course_id)

        assignments = self.assignment_repo.get_assignments_by_module(module_id)

        student_ids = [s.student_id for s in students]
        assignments_ids = [s.assignment_id for s in assignments]
        
        performance_report = self.student_assignment_repo.get_by_student_and_assignment(student_ids, assignments_ids)

        return performance_report
    
    

    
    def get_average_attendance(self, course_id: int | None = None, module_id: int | None = None):
        """Return the percentage of attended sessions out of all scheduled sessions.

        """
        # Case: both course_id and module_id provided -> module-level attendance (float)
        if course_id is not None and module_id is not None:
            if not self.module_repo.is_module_in_course(module_id, course_id):
                raise ValueError("Module does not belong to course")
            return self.calculate_attendance_percentage(module_id=module_id, course_id=course_id)

        # Case: course_id provided only -> overall attendance for the course (float)
        if course_id is not None and module_id is None:
            modules = self.get_modules_for_course(course_id)
            present_count = 0
            total_count = 0
            for module in modules:
                attendance_reports = self.get_attendance_report_for_module(module.module_id, course_id)
                for rec in attendance_reports:
                    total_count += 1
                    if rec.status:
                        present_count += 1
            return (present_count / total_count) * 100 if total_count > 0 else 0.0

        # Case: no course_id -> return overall attendance across all courses (single float)
        # Use all student session records to compute a global attendance percentage
        student_sessions = self.student_session_repo.get_all()
        if not student_sessions:
            return 0.0

        total = len(student_sessions)
        present = sum(1 for s in student_sessions if s.status)
        return (present / total) * 100 if total > 0 else 0.0

    

    def calculate_performance_average(self, module_id: int, course_id) -> float:
        """Calculate average grade for a module (ignores None grades)."""
        student_assignments = self.get_performance_report_for_module(module_id, course_id)
        if not student_assignments:
            return 0.0

        total = 0.0
        count = 0
        for sa in student_assignments:
            if sa.grade is None:
                continue
            total += sa.grade
            count += 1

        return (total / count) if count > 0 else 0.0


    def get_average_performance(self, course_id: int | None = None, module_id: int | None = None):
        """Return average performance (grade) following the same semantics as attendance:

        - No `course_id`: return overall average grade across all student assignments (float).
        - `course_id` only: return overall average grade for that course across its modules (float).
        - `course_id` + `module_id`: return average grade for that module in that course (float).
        """
        # Module-level when both IDs provided
        if course_id is not None and module_id is not None:
            if not self.module_repo.is_module_in_course(module_id, course_id):
                raise ValueError("Module does not belong to course")
            return self.calculate_performance_average(module_id=module_id, course_id=course_id)

        # Course-level overall (aggregate across modules in the course)
        if course_id is not None and module_id is None:
            modules = self.get_modules_for_course(course_id)
            total = 0.0
            count = 0
            for module in modules:
                perf = self.get_performance_report_for_module(module.module_id, course_id)
                for sa in perf:
                    if sa.grade is None:
                        continue
                    total += sa.grade
                    count += 1
            return (total / count) if count > 0 else 0.0

        # No course_id -> overall average across all student assignments
        all_sa = self.student_assignment_repo.get_all()
        total = 0.0
        count = 0
        for sa in all_sa:
            if sa.grade is None:
                continue
            total += sa.grade
            count += 1
        return (total / count) if count > 0 else 0.0
    


    def get_averages(self, course_id: int | None = None, module_id: int | None = None) -> Dict[str, float]:
        """
        Return both average attendance and average performance as a dictionary.

        Keys:
            - 'attendance': float (percentage)
            - 'performance': float (average grade)
        """
        attendance = self.get_average_attendance(course_id=course_id, module_id=module_id)
        performance = self.get_average_performance(course_id=course_id, module_id=module_id)

        return {
            "attendance": attendance,
            "performance": performance
        }

    
