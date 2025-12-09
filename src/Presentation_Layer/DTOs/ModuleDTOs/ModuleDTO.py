from pydantic import BaseModel

class ModuleDTO(BaseModel):
    module_name: str
    credits: int
    module_leader: str
