from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.Data_Access_Layer.DB import get_db
from src.Business_Logic_layer.Services.SessionServices import SessionServices
from src.Business_Logic_layer.Services.CourseServices import CourseServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.WellbeingServices import WellbeingServices
from src.Business_Logic_layer.Services.ModuleServices import ModuleServices
from src.Business_Logic_layer.Services.AssignmentServices import AssignmanetServices
from src.Business_Logic_layer.Services.StudentsServices import StudentsServices
from src.Presentation_Layer.DTOs.ModuleDTOs.ModuleDTO import ModuleDTO
from src.Presentation_Layer.DTOs.CourseDTOs.UpdateCourse import UpdateCourseDTO 
from src.Presentation_Layer.DTOs.SessionDTOs.UpdateSessionDTO import UpdateSessionDTO



router = APIRouter()

@router.get("/CRUD/module/getall/{course_id}")
def get_Modules_by_CourseID(course_id, db: Session = Depends(get_db)):
    service = CourseServices(db)
    return service.get_modules_by_course_id(course_id)

# @router.get("/CRUD/module/getall")
# def getall_modules(db: Session = Depends(get_db)):
#     service = ModuleServices(db)
#     return service.get_all()


@router.post("/CRUD/module/create/{course_id}")
def create_module(course_id, moduleDTO: ModuleDTO  ,db: Session = Depends(get_db)):
    service = ModuleServices(db)
    return service.create(moduleDTO,course_id)

@router.put("/CRUD/module/update/{module_id}")
def update_module(module_id, moduleDTO: ModuleDTO ,db: Session = Depends(get_db)):
    service = ModuleServices(db)
    return service.update(moduleDTO,module_id)

@router.delete("/CRUD/module/delete/{module_id}")
def delete_module(module_id, db: Session = Depends(get_db)):
    service = ModuleServices(db)
    return service.delete(module_id)
