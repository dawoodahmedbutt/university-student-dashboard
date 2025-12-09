from typing import List, Dict
from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo
from src.Data_Access_Layer.Repositories.StudentsSessionRepo import StudentSessionRepo
from src.Data_Access_Layer.Repositories.StudentAssignmentRepo import StudentAssignmentRepo
from src.Data_Access_Layer.Repositories.SessionRepo import SessionRepo
from src.Data_Access_Layer.Repositories.AssignmentRepo import AssignmentRepo
from src.Data_Access_Layer.Repositories.ModuleRepo import ModuleRepo
from src.Domain_Layer.Entities.Module import Module as ModuleEntity

class BarPlotService:
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


    def calculate_attendance_percentage(self, module_id: int,course_id) -> float:
        """Calculate average attendance % for a module."""
        student_sessions = self.get_attendance_report_for_module(module_id, course_id)
        if not student_sessions:
            return 0.0
        
        total_sessions = len(student_sessions)
        present_count = sum(1 for s in student_sessions if s.status == True)
        
        return (present_count / total_sessions) * 100 if total_sessions > 0 else 0.0
    
    def calculate_performance_percentage(self, module_id: int,course_id) -> float:
        """Calculate average attendance % for a module."""
        student_assignments = self.get_performance_report_for_module(module_id, course_id)
        if not student_assignments:
            return 0.0
        
        total_assignments = len(student_assignments)
        performance = sum(s.grade for s in student_assignments)

        
        return performance/total_assignments
    
    

       

    def get_barplot_data(self, course_id: int) -> List[Dict]:
        """
        Returns a list of dictionaries for each module in a course:
        [
            {"module_name": "Module1", "attendance": 90.0, "performance": 85.0},
            ...
        ]
        """
        modules = self.get_modules_for_course(course_id)
        data = []
        
        for module in modules:
            attendance = self.calculate_attendance_percentage(module.module_id, course_id)
            performance = self.calculate_performance_percentage(module.module_id, course_id)
            data.append({
                "module_name": module.module_name,
                "attendance": attendance,
                "performance": performance
            })
        
        return data