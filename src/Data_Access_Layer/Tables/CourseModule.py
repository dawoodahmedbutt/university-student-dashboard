
from sqlalchemy import Table, Column, Integer, ForeignKey
from src.Data_Access_Layer.Base import Base


course_modules = Table(
    "course_modules",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.course_id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("modules.module_id"), primary_key=True)
)
