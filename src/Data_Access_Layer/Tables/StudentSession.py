from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint, Boolean
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
# from API.Data_Access_Layer.Tables.Student import Student 
# from API.Data_Access_Layer.Tables.Session import Session 


# Junction table: Student <-> Session
class StudentSession(Base):
    __tablename__ = "student_sessions"

    st_se_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    status = Column(Boolean)  # e.g., present(True)(1)/absent(False)(0))

    __table_args__ = (UniqueConstraint("student_id", "session_id", name="uq_student_session"),)

    student = relationship("Student", back_populates="student_sessions")
    session = relationship("Session", back_populates="student_sessions")