from collections import defaultdict
from typing import List, Dict
from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo
from src.Data_Access_Layer.Repositories.StudentsSessionRepo import StudentSessionRepo
from src.Data_Access_Layer.Repositories.StudentAssignmentRepo import StudentAssignmentRepo
from src.Data_Access_Layer.Repositories.SessionRepo import SessionRepo
from src.Data_Access_Layer.Repositories.AssignmentRepo import AssignmentRepo
from src.Data_Access_Layer.Repositories.ModuleRepo import ModuleRepo
from src.Domain_Layer.Entities.Module import Module as ModuleEntity

class Gradedistributionservice:
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
    

    def get_performance_report_for_module(self, module_id: int, course_id: int):
        if not self.module_repo.is_module_in_course(module_id, course_id):
            raise ValueError("Module does not belong to course")

        students = self.student_repo.get_students_by_course(course_id)

        assignments = self.assignment_repo.get_assignments_by_module(module_id)

        student_ids = [s.student_id for s in students]
        assignments_ids = [s.assignment_id for s in assignments]
        
        performance_report = self.student_assignment_repo.get_by_student_and_assignment(student_ids, assignments_ids)

        return performance_report    

    
    def get_grade_data(self, module_id: int, course_id) -> Dict[int, float]:
        """Return per-student average grade for all assignments in a module.

        Returns a dict mapping `student_id` -> average grade. Grades that are None
        are ignored. If no grades are available an empty dict is returned.
        """
        student_assignments = self.get_performance_report_for_module(module_id, course_id)
        if not student_assignments:
            return {}

        sums = defaultdict(float)
        counts = defaultdict(int)

        #skip missing grades
        for sa in student_assignments:
            if sa.grade is None:
                continue
            sums[sa.student_id] += sa.grade
            counts[sa.student_id] += 1

        # Compute averages deterministically for student_ids that have counts
        avg_by_student: Dict[int, float] = {
            sid: (sums[sid] / counts[sid]) for sid in sorted(sums.keys()) if counts[sid] > 0
        }

        return avg_by_student
    
    

