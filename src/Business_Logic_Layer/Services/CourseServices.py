from src.Data_Access_Layer.Repositories.CourseRepo import CourseRepo
from src.Domain_Layer.Entities.Course import Course
from datetime import date, time
from sqlalchemy.exc import IntegrityError

class CourseServices:
    def __init__(self, db):
        self.repo = CourseRepo(db)

    def get_all(self):
        res = self.repo.get_all()
        return res     
    def get_course_names(self):
        res = self.repo.get_all()
        return [{"id": course.course_id, "name": course.course_name} for course in res]
    
    def update_course(self,courseDTO, course_id):
        course = Course(course_id, courseDTO.course_name, 
                        courseDTO.course_director, courseDTO.education_level)
        res = self.repo.update(course, course_id)
        return res
    
    def create_course(self,CourseDTO):
        course = Course(None, CourseDTO.course_name, CourseDTO.course_director, CourseDTO.education_level)
        try:
            res = self.repo.add(course)
            return {"success": True, "course": res}
        except IntegrityError as e:
            # Detect unique constraint failure on course name
            orig = getattr(e, "orig", None)
            msg = str(orig) if orig is not None else str(e)
            if "unique" in msg.lower():
                return {"success": False, "message": f"Course name '{CourseDTO.course_name}' already exists."}
            # Re-raise if it's some other integrity issue
            raise
    
    def delete_course(self, course_id):
        res = self.repo.delete(course_id)
        return res
    
    def get_modules_by_course_id(self, course_id: int):
        course = self.repo.get_by_id(course_id)
        modules = course.modules
        return [{"id": module.module_id, "name": module.module_name, "credits": module.credits, "leader": module.module_leader} for module in modules]   
        