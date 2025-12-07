from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment 


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    assignment_name = Column(String(255))
    due_date = Column(Date)

    module = relationship("Module", back_populates="assignments")
    student_assignments = relationship("StudentAssignment", back_populates="assignment", cascade="all, delete-orphan")