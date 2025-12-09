from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.Data_Access_Layer.DB import get_db
from src.Business_Logic_layer.Services.SessionServices import SessionServices
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.CourseServices import CourseServices
from src.Business_Logic_layer.Services.AssignmentServices import AssignmanetServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Presentation_Layer.DTOs.CourseDTOs.CourseDTO import CourseDTO
from src.Presentation_Layer.DTOs.WellbeingDTO.WellbeingDTO import WellbeingDTO
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO



router = APIRouter()

@router.get("/wellbeing/getall")
def get_Wellbeing(course_id: int | None = None, db: Session = Depends(get_db)):
    service = WellbeingServices(db)
    return service.get_all_by_course(course_id)

@router.get("/wellbeing/stress_avg_plot")
def get_stress_avg_plot(db: Session = Depends(get_db)):
    service = WellbeingServices(db)
    return service.stress_avg_plot()

@router.post("/wellbeing/create")
def create_wellbeing(wellbeingDTO: WellbeingDTO, db: Session = Depends(get_db)):
    service = WellbeingServices(db)
    return service.create(wellbeingDTO)
