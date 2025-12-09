# create_db.py

from sqlalchemy import create_engine
from src.Data_Access_Layer.Base import Base

# IMPORTANT — import each table model so Base registers them
from src.Data_Access_Layer.Tables import Course
from src.Data_Access_Layer.Tables import Assignment
from src.Data_Access_Layer.Tables import Wellbeing
from src.Data_Access_Layer.Tables import AuditLogin
from src.Data_Access_Layer.Tables import CourseModule
from src.Data_Access_Layer.Tables import Module
from src.Data_Access_Layer.Tables import Session
from src.Data_Access_Layer.Tables import Student
from src.Data_Access_Layer.Tables import StudentAssignment
from src.Data_Access_Layer.Tables import UserAccount
from src.Data_Access_Layer.Tables import StudentSession
# ... import ALL tables here

engine = create_engine("sqlite:///university.db", echo=True)  # echo=True shows SQL logs
Base.metadata.create_all(engine)

print("Database tables created in university.db")
