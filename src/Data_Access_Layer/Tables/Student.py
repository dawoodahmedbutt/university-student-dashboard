from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing 
from src.Data_Access_Layer.Tables.Course import Course 
from src.Data_Access_Layer.Tables.StudentSession import StudentSession 




class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    address = Column(Text)
    email = Column(String(255), unique=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    year_of_study = Column(Integer)

    # relationships
    wellbeing = relationship("Wellbeing", back_populates="student", cascade="all, delete-orphan")
    course = relationship("Course", back_populates="students")
    student_sessions = relationship("StudentSession", back_populates="student", cascade="all, delete-orphan")
    student_assignments = relationship("StudentAssignment", back_populates="student", cascade="all, delete-orphan")