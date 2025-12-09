from pydantic import BaseModel
from datetime import time, date

class SessionDTO(BaseModel):
    module_id: int           # ID of the module this session belongs to
    start_time: time         # Start time of the session
    end_time: time           # End time of the session
    date: date               # Date of the session
    location: str
