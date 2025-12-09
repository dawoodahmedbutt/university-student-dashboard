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
from src.Presentation_Layer.DTOs.SessionDTOs.SessionDTO import SessionDTO
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO



router = APIRouter()

@router.post("/sessions/create")
def create_session(s: SessionDTO, db: Session = Depends(get_db)):
    service = SessionServices(db)
    return service.create(
        module_id=s.module_id,
        start_time=s.start_time,
        end_time=s.end_time,
        session_date=s.date,
        location= s.location
    )

@router.post("/sessions/update")
def update_session(s: UpdateSessionDTO, db: Session = Depends(get_db)):
    service = SessionServices(db)
    return service.update(
        id= s.session_id,
        module_id=s.module_id,
        start_time=s.start_time,
        end_time=s.end_time,
        session_date=s.date,
        location= s.location
    )

@router.post("/sessions/delete")
def delete_session(session_id: int = Body(..., embed=True), db: Session = Depends(get_db)):
    service = SessionServices(db)
    return service.delete(
        id= session_id
    )

@router.get("/sessions/get/{session_id}")
def get_session_id(session_id: int , db: Session = Depends(get_db)):
    service = SessionServices(db)
    return service.get_id(
        id= session_id
    )

@router.get("/sessions/getall")
def get_all( db: Session = Depends(get_db)):
    service = SessionServices(db)
    return service.get_all()

@router.get("/modules/getall")
def get_all( db: Session = Depends(get_db)):
    service = ModuleServices(db)
    return service.get_all()

@router.get("/wellbeings/getall")
def get_all( db: Session = Depends(get_db)):
    service = WellbeingServices(db)
    return service.get_all()

@router.get("/courses/getall")
def get_all( db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.get_all()

@router.get("/assignments/getall")
def get_all( db: Session = Depends(get_db)):
    service = AssignmanetServices(db)
    return service.get_all()

@router.get("/students/getall")
def get_all( db: Session = Depends(get_db)):
    service = StudentsServices(db)
    return service.get_all()

# @router.get("/explorer/get/tabledropdowns")
# def get_table_dropdowns( db: Session = Depends(get_db)):

#     return [
#         {"teble_id": 1, "table_name": "students"},
#         {"teble_id": 2, "table_name": "courses"},
#         {"teble_id": 3, "table_name": "modules"}
#     ]

