from collections import defaultdict
from typing import List, Dict
from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo
from src.Data_Access_Layer.Repositories.StudentsSessionRepo import StudentSessionRepo
from src.Data_Access_Layer.Repositories.StudentAssignmentRepo import StudentAssignmentRepo
from src.Data_Access_Layer.Repositories.SessionRepo import SessionRepo
from src.Data_Access_Layer.Repositories.AssignmentRepo import AssignmentRepo
from src.Data_Access_Layer.Repositories.ModuleRepo import ModuleRepo
from src.Domain_Layer.Entities.Module import Module as ModuleEntity

class Studentriskservice:
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

    def get_attendance_report_for_module(self, module_id: int, course_id: int):
        if not self.module_repo.is_module_in_course(module_id, course_id):
            raise ValueError("Module does not belong to course")

        students = self.student_repo.get_students_by_course(course_id)

        sessions = self.session_repo.get_sessions_by_module(module_id)

        student_ids = [s.student_id for s in students]
        session_ids = [s.session_id for s in sessions]
        
        attendance_report = self.student_session_repo.get_attendance_for(student_ids, session_ids)

        return attendance_report  

    
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
    
        
    def get_attendance_data(self, module_id: int, course_id) -> Dict[int, float]:
        """Return per-student average attendance for all assignments in a module.

        Returns a dict mapping `student_id` -> average attendance. Attendance that are None
        are ignored. If no attendance records are available an empty dict is returned.
        """
        student_sessions = self.get_attendance_report_for_module(module_id, course_id)
        if not student_sessions:
            return {}

        present = defaultdict(float)
        total = defaultdict(int)

        #skip missing status
        for ss in student_sessions:
            if ss.status is None:
                continue
            if ss.status == 1:
                present[ss.student_id] += 1
            total[ss.student_id] += 1

        # Compute averages deterministically for student_ids that have counts
        avg_by_student: Dict[int, float] = {
            sid: (present[sid] / total[sid]) for sid in sorted(present.keys()) if total[sid] > 0
        }

        return avg_by_student
    

    def classify_risk(self, attendance: float, performance: float) -> str:
        """Classify student risk using simple rule-based thresholds."""
        combined = (attendance + performance) / 2

        # High Risk
        if attendance < 60 or performance < 50 or combined < 55:
            return "HIGH"

        # Medium Risk
        if attendance < 75 or performance < 65 or combined < 70:
            return "MEDIUM"

        # Low Risk
        return "LOW"


    def get_student_risk_summary(self, module_id: int, course_id: int) -> Dict[int, Dict]:
        """
        Returns:
        {
            student_id: {
                "attendance": float (0–100),
                "performance": float (0–100),
                "risk": "HIGH" | "MEDIUM" | "LOW"
            }
        }
        """

        # Get per-student data
        performance = self.get_grade_data(module_id, course_id)      # 0–100
        attendance_raw = self.get_attendance_data(module_id, course_id)  # 0–1

        # Convert attendance to percentage
        attendance = {sid: (val * 100) for sid, val in attendance_raw.items()}

        # Get all students in the course (map id -> student)
        students = self.student_repo.get_students_by_course(course_id)
        students_map = {s.student_id: s for s in students}

        # Filter to students who actually appear in the module (attendance or performance)
        module_student_ids = set(performance.keys()) | set(attendance_raw.keys())
        # Ensure students are enrolled in the course
        module_student_ids = [sid for sid in sorted(module_student_ids) if sid in students_map]

        result = {}
        for sid in module_student_ids:
            att = attendance.get(sid, 0.0)
            perf = performance.get(sid, 0.0)

            risk = self.classify_risk(attendance=att, performance=perf)

            student = students_map.get(sid)
            first_name = f"{getattr(student, 'first_name', '')}".strip()
            last_name = f"{getattr(student, 'last_name', '')}".strip()

            result[sid] = {
                "first_name": first_name,
                "last_name": last_name,
                "attendance": round(att, 2),
                "performance": round(perf, 2),
                "risk": risk
            }

        return result

    
    

