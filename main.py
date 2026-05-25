from fastapi import FastAPI
import uvicorn

# Import all table classes to ensure SQLAlchemy mapper configuration
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.Session import Session
from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment
from src.Data_Access_Layer.Tables.StudentSession import StudentSession
from src.Data_Access_Layer.Tables.UserAccount import UserAccount
from src.Data_Access_Layer.Tables.AuditLogin import AuditLogin
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing
from src.Data_Access_Layer.Tables.CourseModule import course_modules

from src.Presentation_Layer.Routers.ExplorerDashboard import router as ExplorerDashboard_router
from src.Presentation_Layer.Routers.DirectorDashboard import router as DirectorDashboard_router
from src.Presentation_Layer.Routers.CRUDDashboard.CourseTable import router as Course_table_router 
from src.Presentation_Layer.Routers.CRUDDashboard.ModuleTable import router as Module_table_router 
from src.Presentation_Layer.Routers.CRUDDashboard.StudentTable import router as Student_table_router 
from src.Presentation_Layer.Routers.WellbeingDashboard import router as WellbeingDashboard_router 
from src.Presentation_Layer.Routers.LoginDashboard import router as LoginDashboard_router


app = FastAPI(title="Student System API")


app.include_router(ExplorerDashboard_router, tags=["Explorer"])
app.include_router(DirectorDashboard_router, tags=["Director"])
app.include_router(Course_table_router, tags=["Course_table_crud"])
app.include_router(Module_table_router, tags=["Module_table_crud"])
app.include_router(Student_table_router, tags=["Student_table_crud"])
app.include_router(WellbeingDashboard_router, tags=["WellbeingDashboard"])
app.include_router(LoginDashboard_router, tags=["LoginDashboard"])

@app.get("/")
def home():
    return {"message": "Student System API running"}

