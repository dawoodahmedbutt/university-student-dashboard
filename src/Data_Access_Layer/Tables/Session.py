from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Tables.Module import Module 
from src.Data_Access_Layer.Base import Base



class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"))
    session_location = Column(String(200))
    session_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    module = relationship("Module", back_populates="sessions")
    student_sessions = relationship("StudentSession", back_populates="session", cascade="all, delete-orphan")