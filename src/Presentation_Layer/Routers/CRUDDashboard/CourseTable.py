from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.Data_Access_Layer.DB import get_db
from src.Business_Logic_layer.Services.SessionServices import SessionServices
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.CourseServices import CourseServices
from src.Business_Logic_layer.Services.AssignmentServices import AssignmanetServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Presentation_Layer.DTOs.CourseDTOs.CourseDTO import CourseDTO
from src.Presentation_Layer.DTOs.CourseDTOs.UpdateCourse import UpdateCourseDTO 
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO



router = APIRouter()

@router.get("/CRUD/course/getall")
def get_Courses(db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.get_all()


@router.post("/CRUD/course/create")
def create_course(courseDTO: CourseDTO ,db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.create_course(courseDTO)

@router.put("/CRUD/course/update/{course_id}")
def update_course(course_id, courseDTO: CourseDTO ,db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.update_course(courseDTO,course_id)

@router.delete("/CRUD/course/delete/{course_id}")
def delete_course(course_id, db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.delete_course(course_id)
