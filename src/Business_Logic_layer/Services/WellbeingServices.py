from src.Domain_Layer.Entities.Wellbeing import Wellbeing
from src.Data_Access_Layer.Repositories.WellbeingRepo import WellbeingRepo
from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo 
from src.Data_Access_Layer.Repositories.CourseRepo import CourseRepo
from src.Exceptions.WellbeingExceptions import WellbeingException

class WellbeingServices:
    def __init__(self, db):
        self.db = db
        self.repo = WellbeingRepo(db)
        self.student_repo = StudentRepo(db)
        self.course_repo = CourseRepo(db)

    def create(self,wellbeingDTO):        
        wellbeing = Wellbeing(None, wellbeingDTO.student_id, wellbeingDTO.date, wellbeingDTO.stress, wellbeingDTO.activity, wellbeingDTO.food_quality,
                 wellbeingDTO.alcohol_drugs, wellbeingDTO.medication, wellbeingDTO.hours_slept)
        res = self.repo.add(wellbeing)
        if res:
            return {"success": True, "wellbeing": res}
        else:
            return {"success": False, "message": "Failed to create wellbeing data."}
    
    def update(self, id, student_id, date, stress, activity, food_quality,
                 alcohol_drugs, hours_slept, comment):
        wellbeing = Wellbeing(id,student_id, date,stress,activity,food_quality, alcohol_drugs, hours_slept, comment )
        if wellbeing is None:
            raise WellbeingException(f"Wellbeing data with id = {id} is not existed ")
        return True
    
    def delete(self, id):
        if not self.repo.delete(id):
            raise WellbeingException("Can't find wellbeing id")
        return True
    
    def get_id(self, id: int):

        wellbeing = self.repo.get_by_id(id)
        if wellbeing is None:
            raise WellbeingException(f"id = {id} not found")
        return wellbeing
    
    def get_all(self):
        res = self.repo.get_all()
        for student in res:
            student_name = self.student_repo.get_student_name_by_id(student.student_id)
            student.student_first_name =  student_name["first_name"]
            student.student_last_name = student_name["last_name"]
            student.risk_level = (student.stress_level + (10 - student.activity_level)
                                + (10 - student.quality_of_food) + student.alcohol_drug_consumption + student.medication) / 5
        return res
    
    def get_all_by_course(self, course_id: int):
        if course_id is None:
            return self.get_all()
        else:
            students = self.student_repo.get_students_by_course(course_id)
            student_ids = [student.student_id for student in students]
            res = self.repo.get_all_by_studentIDs(student_ids)
            for student in res:
                student_name = self.student_repo.get_student_name_by_id(student.student_id)
                student.student_first_name =  student_name["first_name"]
                student.student_last_name = student_name["last_name"]
                student.risk_level = 10 - student.stress_level
            return res
    
    def stress_avg_by_course(self, course_id: int):
        students = self.student_repo.get_students_by_course(course_id)
        student_ids = [student.student_id for student in students]
        wellbeing_data = self.repo.get_all_by_studentIDs(student_ids)
        if not wellbeing_data:
            return 0
        total_stress = sum([data.stress_level for data in wellbeing_data])
        avg_stress = total_stress / len(wellbeing_data)
        return avg_stress
    
    def stress_avg_plot(self):
        courses = self.course_repo.get_all()
        result = []
        for course in courses:
            avg_stress = self.stress_avg_by_course(course.course_id)
            result.append({
                "course_name": course.course_name,
                "avg_stress": round(avg_stress, 2)
            })
        return result
    
    
        
