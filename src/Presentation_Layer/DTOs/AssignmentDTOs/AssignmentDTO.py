from pydantic import BaseModel
from datetime import date

class AssignmentDTO(BaseModel):
    module_id: int
    assignment_name: str
    due_date: date
    max_marks: int
