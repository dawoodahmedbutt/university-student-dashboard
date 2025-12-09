from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint,CheckConstraint
)
from sqlalchemy.orm import relationship
from src.Data_Access_Layer.Base import Base
# from API.Data_Access_Layer.Tables.Student import Student 


class Wellbeing(Base):
    __tablename__ = "wellbeing"

    wellbeing_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    date = Column(Date)
    stress_level = Column(Integer, nullable=False)
    activity_level = Column(Integer, nullable=False)
    quality_of_food = Column(Integer, nullable=False)
    alcohol_drug_consumption = Column(Integer, nullable=False)
    medication = Column(Integer, nullable=False)
    hours_slept = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("stress_level BETWEEN 1 AND 10", name="check_stress"),
        CheckConstraint("activity_level BETWEEN 1 AND 10", name="check_activity"),
        CheckConstraint("quality_of_food BETWEEN 1 AND 10", name="check_food_quality"),
        CheckConstraint("alcohol_drug_consumption BETWEEN 1 AND 10", name="check_alcohol_drug"),
        CheckConstraint("medication BETWEEN 1 AND 10", name="check_medication"),
        CheckConstraint("hours_slept BETWEEN 0 AND 24", name="check_sleep"),
        UniqueConstraint("student_id", "date", name="unique_student_date"),
    )   

    student = relationship("Student", back_populates="wellbeing")