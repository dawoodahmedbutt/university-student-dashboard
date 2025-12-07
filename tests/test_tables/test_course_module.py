import pytest
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Module import Module

# Tests for Course table
def test_create_course(session):
    course = Course(
        course_name="Computer Science",
        course_director="Dr. Smith",
        education_level="Undergraduate"
    )
    session.add(course)
    session.commit()

    db_course = session.query(Course).filter_by(course_name="Computer Science").first()
    assert db_course is not None
    assert db_course.course_name == "Computer Science"
    assert db_course.course_director == "Dr. Smith"
    assert db_course.education_level == "Undergraduate"

def test_course_name_unique_constraint(session):
    # Adding a course with the same name should raise an IntegrityError
    course1 = Course(course_name="Mathematics", course_director="Dr. A", education_level="Undergraduate")
    session.add(course1)
    session.commit()

    from sqlalchemy.exc import IntegrityError
    course2 = Course(course_name="Mathematics", course_director="Dr. B", education_level="Undergraduate")
    session.add(course2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

# Tests for Module table
def test_create_module(session):
    module = Module(
        module_name="Databases",
        credits=20,
        module_leader="Prof. Lee"
    )
    session.add(module)
    session.commit()

    db_module = session.query(Module).filter_by(module_name="Databases").first()
    assert db_module is not None
    assert db_module.credits == 20
    assert db_module.module_leader == "Prof. Lee"

def test_module_name_unique_constraint(session):
    module1 = Module(module_name="Algorithms", credits=15, module_leader="Prof. X")
    session.add(module1)
    session.commit()

    from sqlalchemy.exc import IntegrityError
    module2 = Module(module_name="Algorithms", credits=15, module_leader="Prof. Y")
    session.add(module2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

# Tests for Course Module relationship
def test_course_module_relationship(session):
    course = Course(course_name="Software Engineering", course_director="Dr. Brown", education_level="Undergraduate")
    module = Module(module_name="Software Design", credits=15, module_leader="Prof. White")
    session.add_all([course, module])
    session.commit()

    course.modules.append(module)
    session.commit()

    db_course = session.query(Course).filter_by(course_name="Software Engineering").first()
    db_module = session.query(Module).filter_by(module_name="Software Design").first()
    assert db_module in db_course.modules
    assert db_course in db_module.courses

def test_update_course(session):
    course = Course(course_name="Physics", course_director="Dr. Newton", education_level="Undergraduate")
    session.add(course)
    session.commit()

    course.course_director = "Dr. Einstein"
    session.commit()

    db_course = session.query(Course).filter_by(course_name="Physics").first()
    assert db_course.course_director == "Dr. Einstein"

def test_delete_module(session):
    module = Module(module_name="Operating Systems", credits=20, module_leader="Prof. Kernel")
    session.add(module)
    session.commit()

    session.delete(module)
    session.commit()

    db_module = session.query(Module).filter_by(module_name="Operating Systems").first()
    assert db_module is None

def test_course_multiple_modules(session):
    course = Course(course_name="Engineering", course_director="Dr. Eng", education_level="Undergraduate")
    module1 = Module(module_name="Statics", credits=10, module_leader="Prof. Stat")
    module2 = Module(module_name="Dynamics", credits=10, module_leader="Prof. Dyn")
    session.add_all([course, module1, module2])
    session.commit()

    course.modules.extend([module1, module2])
    session.commit()

    db_course = session.query(Course).filter_by(course_name="Engineering").first()
    assert module1 in db_course.modules
    assert module2 in db_course.modules

def test_query_courses_by_module(session):
    module = Module(module_name="Networking", credits=10, module_leader="Prof. Net")
    course1 = Course(course_name="CS", course_director="Dr. A", education_level="Undergraduate")
    course2 = Course(course_name="IT", course_director="Dr. B", education_level="Undergraduate")
    session.add_all([module, course1, course2])
    session.commit()

    module.courses.extend([course1, course2])
    session.commit()

    db_module = session.query(Module).filter_by(module_name="Networking").first()
    course_names = [c.course_name for c in db_module.courses]
    assert "CS" in course_names
    assert "IT" in course_names