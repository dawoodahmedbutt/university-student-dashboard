from pydantic import BaseModel

class CourseDTO(BaseModel):
    course_name: str
    education_level: str
    course_director: str | None = None   # optional
