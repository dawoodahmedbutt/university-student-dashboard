from pydantic import BaseModel

class SubmissionDTO(BaseModel):
    student_id: int
    assignment_id: int
