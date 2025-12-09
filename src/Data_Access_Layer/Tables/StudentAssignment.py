from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint, FLOAT,BOOLEAN
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
from src.Data_Access_Layer.Tables.Student import Student 
# from API.Data_Access_Layer.Tables.Assignment import Assignment 


# Junction table: Student <-> Assignment
class StudentAssignment(Base):
    __tablename__ = "student_assignments"


    st_as_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    submitted_date = Column(DateTime)
    grade = Column(FLOAT)


    __table_args__ = (UniqueConstraint("student_id", "assignment_id", name="uq_student_assignment"),)


    student = relationship("Student", back_populates="student_assignments")
    assignment = relationship("Assignment", back_populates="student_assignments")