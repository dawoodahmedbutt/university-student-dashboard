from pydantic import BaseModel
from datetime import date as datee


class WellbeingDTO(BaseModel):
    student_id: int
    date: datee
    stress: int
    activity: int
    food_quality: int
    alcohol_drugs: int
    medication: int
    hours_slept: int