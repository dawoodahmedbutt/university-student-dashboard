from src.Data_Access_Layer.Repositories.StudentRepo import StudentRepo
from src.Data_Access_Layer.Repositories.CourseRepo import CourseRepo
from src.Domain_Layer.Entities.Student import Student
from datetime import date, time
from sqlalchemy.exc import IntegrityError

class StudentsServices:
    def __init__(self, db):
        self.student_repo = StudentRepo(db)
        self.course_repo = CourseRepo(db)

    def get_all(self):
        res = self.student_repo.get_all()
        for student in res:
            course = self.course_repo.get_by_id(student.course_id)
            if course:
                student.course_name = course.course_name
        return res 

    def create(self, studentDTO):
        student = Student(None,studentDTO.first_name,studentDTO.last_name, studentDTO.address
                          , studentDTO.course_id, studentDTO.year_of_study, studentDTO.email)
        course = self.course_repo.get_by_id(studentDTO.course_id)
        if course is None:
            raise Exception(f"no course id = {studentDTO.course_id} existed")
        try:
            res = self.student_repo.add(student)
            return {"success": True, "student": res}
        except IntegrityError as e:
            # detect unique constraint violation (SQLite/other DBs)
            orig = getattr(e, 'orig', None)
            msg = str(orig) if orig is not None else str(e)
            if 'unique' in msg.lower() or 'unique constraint' in msg.lower() or 'unique constraint failed' in msg.lower() or 'UNIQUE constraint failed' in msg:
                # return a friendly message instead of raising
                return {"success": False, "message": f"A student with email {studentDTO.email} already exists."}
            raise
    
    def update(self, studentDTO, student_id):
        student = Student(student_id,studentDTO.first_name,
                          studentDTO.last_name, studentDTO.address
                          , studentDTO.course_id, studentDTO.year_of_study, studentDTO.email)
        res = self.student_repo.update(student, student_id)
        return res
    
    def delete(self, student_id):
        res = self.student_repo.delete(student_id)
        return res