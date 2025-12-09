from pydantic import BaseModel

class GradeSubmissionDTO(BaseModel):
    student_id: int
    assignment_id: int
    grade: int
