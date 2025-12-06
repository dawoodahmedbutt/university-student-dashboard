import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Data_Access_Layer.Base import Base

# Import all table classes
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.CourseModule import course_modules
from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Session import Session
from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.StudentSession import StudentSession

@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="module")
def setup_db(engine):

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, setup_db):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
