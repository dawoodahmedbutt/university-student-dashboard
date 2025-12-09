from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.Data_Access_Layer.DB import get_db
from src.Business_Logic_layer.Services.SessionServices import SessionServices
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Business_Logic_layer.Services.AssignmentServices import AssignmanetServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Presentation_Layer.DTOs.StudentDTOs.StudentDTO import StudentDTO
from src.Presentation_Layer.DTOs.CourseDTOs.UpdateCourse import UpdateCourseDTO 
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO



router = APIRouter()

@router.get("/CRUD/student/getall")
def Students(db: Session = Depends(get_db)):
    service = StudentsServices(db)
    return service.get_all()


@router.post("/CRUD/student/create")
def create_Student(studentDTO:StudentDTO  ,db: Session = Depends(get_db)):
    service = StudentsServices(db)
    res = service.create(studentDTO)
    return res

@router.put("/CRUD/student/update/{student_id}")
def update_Student(student_id, studentDTO: StudentDTO ,db: Session = Depends(get_db)):
    service = StudentsServices(db)
    return service.update(studentDTO,student_id)

@router.delete("/CRUD/student/delete/{student_id}")
def delete_Student(student_id, db: Session = Depends(get_db)):
    service = StudentsServices(db)
    return service.delete(student_id)
