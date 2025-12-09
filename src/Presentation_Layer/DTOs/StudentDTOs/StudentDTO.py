from pydantic import BaseModel
from datetime import date 

class StudentDTO(BaseModel):
    first_name: str
    last_name: str
    address: str
    email: str
    course_id: int
    year_of_study: int
