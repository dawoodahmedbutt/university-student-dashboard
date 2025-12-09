from pydantic import BaseModel

class AttendanceDTO(BaseModel):
    student_id: int
    session_id: int
    status: str    # "present" / "absent"
