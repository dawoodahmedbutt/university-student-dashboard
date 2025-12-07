from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
from src.Data_Access_Layer.Tables.UserAccount import UserAccount 


class AuditLogin(Base):
    __tablename__ = "audit_logins"


    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_accounts.user_id"))
    timestamp = Column(DateTime)


    user = relationship("UserAccount", back_populates="audit_logs")