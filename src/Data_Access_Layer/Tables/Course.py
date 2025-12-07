from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
from src.Data_Access_Layer.Tables.CourseModule import course_modules 
 




class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(200),unique=True)
    course_director = Column(String(200))
    education_level = Column(String(100))

    students = relationship("Student", back_populates="course")
    modules = relationship("Module", secondary=course_modules, back_populates="courses")
