from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.CourseModule import course_modules 
# from API.Data_Access_Layer.Tables.Session import Session 


 

class Module(Base):
    __tablename__ = "modules"

    module_id = Column(Integer, primary_key=True)
    module_name = Column(String(200), unique= True)
    credits = Column(Integer)
    module_leader = Column(String(200))

    sessions = relationship("Session", back_populates="module", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="module", cascade="all, delete-orphan")
    courses = relationship("Course", secondary=course_modules, back_populates="modules")
