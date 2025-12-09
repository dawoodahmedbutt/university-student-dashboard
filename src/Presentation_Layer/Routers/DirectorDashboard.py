from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.Business_Logic_layer.Services.Studentriskservice import Studentriskservice
from src.Data_Access_Layer.DB import get_db
from src.Business_Logic_layer.Services.SessionServices import SessionServices
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from src.Business_Logic_layer.Services.BarplotService import BarPlotService
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.CourseServices import CourseServices
from src.Business_Logic_layer.Services.AssignmentServices import AssignmanetServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Presentation_Layer.DTOs.SessionDTOs.SessionDTO import SessionDTO
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO
from src.Business_Logic_layer.Services.Gradedistributionservice import Gradedistributionservice
from src.Business_Logic_layer.Services.AveragesService import AveragesService as AveragesService


router = APIRouter()

@router.get("/director/coursesdropdown")
def courses_list_dropdown(db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.get_course_names()

@router.get("/director/moduledropdown/{course_id}")
def modules_list_dropdown(course_id,db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.get_modules_by_course_id(course_id)

@router.get("/director/barplot/{course_id}")
def barplot(course_id: int,db: Session = Depends(get_db)):
    service = BarPlotService(db)
    return service.get_barplot_data(course_id)

@router.get("/director/gradedistribution/{course_id}/{module_id}")
def get_grade_data(course_id: int, module_id: int,db: Session = Depends(get_db)):
    service = Gradedistributionservice(db)
    return service.get_grade_data(module_id, course_id)

@router.get("/director/Averages")
def get_averages(
    course_id: int | None = None,
    module_id: int | None = None,
    db: Session = Depends(get_db)
):
    service = AveragesService(db)
    return service.get_averages(module_id=module_id, course_id=course_id)

@router.get("/director/Studentrisk/{course_id}/{module_id}")
def get_grade_data(course_id: int, module_id: int,db: Session = Depends(get_db)):
    service = Studentriskservice(db)
    return service.get_student_risk_summary(module_id, course_id)


# @router.get("/director/test")
# def test(db: Session = Depends(get_db)):
#     service = ModuleServices(db)
#     return service.get_all()