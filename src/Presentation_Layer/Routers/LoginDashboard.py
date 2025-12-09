from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.Data_Access_Layer.DB import get_db
from src.Business_Logic_layer.Services.SessionServices import SessionServices
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from src.Business_Logic_layer.Services.LoginServices import LoginServices
from src.Business_Logic_layer.Services.CourseServices import CourseServices
from src.Business_Logic_layer.Services.AssignmentServices import AssignmanetServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Presentation_Layer.DTOs.LoginDTO.LoginDTO import LoginDTO
from src.Presentation_Layer.DTOs.CourseDTOs.UpdateCourse import UpdateCourseDTO 
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO



router = APIRouter()

@router.post("/login")
def get_Wellbeing(login: LoginDTO, db: Session = Depends(get_db)):
    service = LoginServices(db)
    return service.log_in(
        loginDTO=login
    )