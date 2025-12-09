# from sqlalchemy import (
#     Column, Integer, String, Date, Time, ForeignKey, Text, DateTime, UniqueConstraint
# )
# from sqlalchemy.orm import relationship
# from API.Data_Access_Layer.Base import Base
# # from API.Data_Access_Layer.Tables.Module import Module 
# from API.Data_Access_Layer.Tables.Course import Course 


# # Junction table: Course <-> Module (Option B: surrogate PK + UNIQUE)
# class CourseModule(Base):
#     __tablename__ = "course_modules"

#     co_mo_id = Column(Integer, primary_key=True)
#     course_id = Column(Integer, ForeignKey("courses.course_id"))
#     module_id = Column(Integer, ForeignKey("modules.module_id"))

#     __table_args__ = (UniqueConstraint("course_id", "module_id", name="uq_course_module"),)

#     course = relationship("Course", back_populates="course_modules")
#     module = relationship("Module", back_populates="course_modules")

from sqlalchemy import Table, Column, Integer, ForeignKey
from src.Data_Access_Layer.Base import Base


course_modules = Table(
    "course_modules",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.course_id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("modules.module_id"), primary_key=True)
)
