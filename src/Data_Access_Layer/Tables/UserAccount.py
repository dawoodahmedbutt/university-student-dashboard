from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base



class UserAccount(Base):
    __tablename__ = "user_accounts"


    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255)) # store hashed password
    role = Column(String(50))


    audit_logs = relationship("AuditLogin", back_populates="user", cascade="all, delete-orphan")