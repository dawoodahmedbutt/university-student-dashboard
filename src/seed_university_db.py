from datetime import date, datetime, time, timedelta
import os
import sys

# ensure repo root is on sys.path so `src` package imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.Data_Access_Layer.DB import engine, SessionLocal
from src.Data_Access_Layer.Base import Base

from src.Data_Access_Layer.Tables.Student import Student
from src.Data_Access_Layer.Tables.Course import Course
from src.Data_Access_Layer.Tables.Module import Module
from src.Data_Access_Layer.Tables.Assignment import Assignment
from src.Data_Access_Layer.Tables.Session import Session
from src.Data_Access_Layer.Tables.StudentAssignment import StudentAssignment
from src.Data_Access_Layer.Tables.StudentSession import StudentSession
from src.Data_Access_Layer.Tables.UserAccount import UserAccount
from src.Data_Access_Layer.Tables.AuditLogin import AuditLogin
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing
from src.Data_Access_Layer.Tables.CourseModule import course_modules


def seed(reset=False):
    # Drop and recreate all tables if reset=True
    if reset:
        Base.metadata.drop_all(bind=engine)
    
    # create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1) Courses - 8 courses
        courses_data = [
            ("Computer Science BSc", "Dr Alice Smith", "Undergraduate"),
            ("Business Management BSc", "Dr Bob Jones", "Undergraduate"),
            ("Psychology BSc", "Prof Emma Wilson", "Undergraduate"),
            ("Engineering MEng", "Dr Frank Cooper", "Postgraduate"),
            ("Mathematics MSc", "Prof Grace Lee", "Postgraduate"),
            ("English Literature BA", "Dr Henry Brown", "Undergraduate"),
            ("Physics BSc", "Dr Iris Kumar", "Undergraduate"),
            ("Economics MSc", "Prof Jack Thompson", "Postgraduate"),
        ]
        courses = []
        for course_name, director, level in courses_data:
            course = Course(course_name=course_name, course_director=director, education_level=level)
            courses.append(course)
        db.add_all(courses)
        db.commit()

        # 2) Modules - 25 modules
        modules_data = [
            # CS modules
            ("Programming 101", 20, "Dr Alan Turing"),
            ("Databases", 15, "Dr Edgar Codd"),
            ("Web Development", 15, "Dr Steve Jobs"),
            ("Data Structures", 20, "Prof Donald Knuth"),
            ("Operating Systems", 20, "Dr Linus Torvalds"),
            ("Machine Learning", 15, "Dr Geoffrey Hinton"),
            ("Software Engineering", 15, "Dr Barry Boehm"),
            # Business modules
            ("Management Principles", 15, "Dr Peter Drucker"),
            ("Marketing Strategy", 15, "Prof Philip Kotler"),
            ("Finance Fundamentals", 20, "Dr Benjamin Graham"),
            ("Business Law", 10, "Prof Richard Posner"),
            ("Organizational Behavior", 15, "Prof Edgar Schein"),
            # Psychology modules
            ("Introduction to Psychology", 20, "Dr Albert Ellis"),
            ("Cognitive Psychology", 15, "Prof Ulric Neisser"),
            ("Social Psychology", 15, "Dr Solomon Asch"),
            # Engineering modules
            ("Thermodynamics", 20, "Prof Ludwig Boltzmann"),
            ("Mechanics", 20, "Prof Isaac Newton"),
            ("Circuit Analysis", 15, "Dr George Ohm"),
            # Math modules
            ("Calculus", 20, "Prof Isaac Newton"),
            ("Linear Algebra", 20, "Prof Emmy Noether"),
            ("Probability Theory", 15, "Dr Andrey Kolmogorov"),
            # English modules
            ("Shakespeare", 15, "Prof Harold Bloom"),
            ("Modern Literature", 15, "Dr James Joyce"),
            # Physics modules
            ("Quantum Mechanics", 20, "Prof Werner Heisenberg"),
            ("Statistics", 10, "Dr Florence Nightingale"),
        ]
        modules = []
        for module_name, credits, leader in modules_data:
            module = Module(module_name=module_name, credits=credits, module_leader=leader)
            modules.append(module)
        db.add_all(modules)
        db.commit()

        # 3) Associate modules with courses (many-to-many)
        # CS course gets modules 0-6
        for mod in modules[0:7]:
            courses[0].modules.append(mod)
        # Business course gets modules 7-11
        for mod in modules[7:12]:
            courses[1].modules.append(mod)
        # Psychology gets 12-14
        for mod in modules[12:15]:
            courses[2].modules.append(mod)
        # Engineering gets 15-17
        for mod in modules[15:18]:
            courses[3].modules.append(mod)
        # Math gets 18-20
        for mod in modules[18:21]:
            courses[4].modules.append(mod)
        # English gets 21-22
        for mod in modules[21:23]:
            courses[5].modules.append(mod)
        # Physics gets 23-24 + 20 (Stats)
        for mod in [modules[23], modules[24], modules[20]]:
            courses[6].modules.append(mod)
        # Economics gets Econ-specific + Stats, Finance
        for mod in [modules[9], modules[20], modules[24]]:
            courses[7].modules.append(mod)
        db.commit()

        # 4) Users and audit logs - 15 users
        user_emails = [
            ("admin@university.edu", "adminpass", "admin"),
            ("director@university.edu", "directorpass", "director"),
            ("lecturer1@university.edu", "pass123", "lecturer"),
            ("lecturer2@university.edu", "pass123", "lecturer"),
            ("lecturer3@university.edu", "pass123", "lecturer"),
            ("lecturer4@university.edu", "pass123", "lecturer"),
            ("lecturer5@university.edu", "pass123", "lecturer"),
            ("support@university.edu", "pass123", "support"),
            ("finance@university.edu", "pass123", "finance"),
            ("registrar@university.edu", "pass123", "registrar"),
            ("health@university.edu", "pass123", "health"),
            ("counselor@university.edu", "pass123", "counselor"),
            ("it_admin@university.edu", "pass123", "admin"),
            ("hr@university.edu", "pass123", "admin"),
            ("security@university.edu", "pass123", "support"),
        ]
        users = []
        for email, password, role in user_emails:
            user = UserAccount(email=email, password=password, role=role)
            users.append(user)
        db.add_all(users)
        db.commit()

        # Add audit logs for users
        audit_logs = []
        for i, user in enumerate(users):
            for day in range(1, 6):  # 5 login events per user
                audit = AuditLogin(user_id=user.user_id, timestamp=datetime(2025, 11, day, 9 + i % 8, 0))
                audit_logs.append(audit)
        db.add_all(audit_logs)
        db.commit()

        # 5) Students - 100 students across courses
        first_names = ["James", "Mary", "Robert", "Patricia", "Michael", "Jennifer", "William", "Linda", "David", "Barbara",
                       "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
                       "Daniel", "Betty", "Matthew", "Margaret", "Anthony", "Sandra", "Mark", "Ashley", "Donald", "Kimberly",
                       "John", "Emily", "Steven", "Donna", "Paul", "Michelle", "Andrew", "Dorothy", "Joshua", "Carol",
                       "Kenneth", "Amanda", "Kevin", "Melissa", "Brian", "Deborah", "George", "Stephanie", "Edward", "Rebecca",
                       "Ronald", "Sharon", "Timothy", "Laura"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                      "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                      "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                      "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Peterson", "Phillips", "Campbell",
                      "Parker", "Evans", "Edwards", "Collins", "Reeves", "Morris", "Murphy", "Rogers", "Morgan", "Peterson"]

        students = []
        student_idx = 0
        for course_idx, course in enumerate(courses):
            students_per_course = 12 + (course_idx % 4)  # 12-15 students per course
            for i in range(students_per_course):
                first = first_names[(student_idx + i) % len(first_names)]
                last = last_names[(student_idx + i) % len(last_names)]
                email = f"{first.lower()}.{last.lower()}{student_idx + i}@student.edu"
                year = 1 + (i % 3)
                student = Student(
                    first_name=first,
                    last_name=last,
                    address=f"{100 + student_idx + i} Student Street",
                    email=email,
                    course_id=course.course_id,
                    year_of_study=year
                )
                students.append(student)
            student_idx += students_per_course
        db.add_all(students)
        db.commit()

        # 6) Wellbeing records - multiple per student across October/November
        wellbeing_records = []
        for student in students:
            for day in range(1, 31):  # Records for Oct 1-30
                wellbeing = Wellbeing(
                    student_id=student.student_id,
                    date=date(2025, 10, day),
                    stress_level=(day * 7 + student.student_id) % 10 + 1,  # 1-10
                    activity_level=(day * 3 + student.student_id * 2) % 10 + 1,  # 1-10
                    quality_of_food=(day * 5 + student.student_id) % 10 + 1,  # 1-10
                    alcohol_drug_consumption=(day + student.student_id) % 10 + 1,  # 1-10
                    medication=(day // 7 + student.student_id) % 10 + 1,  # 1-10
                    hours_slept=(day * 2 + student.student_id) % 17 + 4  # 4-20 (reasonable sleep range)
                )
                wellbeing_records.append(wellbeing)
        db.add_all(wellbeing_records)
        db.commit()

        # 7) Sessions - multiple per module across Nov/Dec
        sessions = []
        session_id_counter = 0
        rooms = ["Room 101", "Room 102", "Room 103", "Room 104", "Room 105", "Lecture Hall A", "Lecture Hall B", "Lab 1", "Lab 2", "Seminar Room"]
        for module in modules:
            for week in range(1, 15):  # 14 weeks of sessions
                for day_offset in [0, 2]:  # 2 sessions per module per week
                    session_date = date(2025, 11, week * 2 + day_offset)
                    if session_date.day > 30:
                        session_date = date(2025, 12, session_date.day - 30)
                    start_h = 9 + (week + session_id_counter) % 8
                    session = Session(
                        module_id=module.module_id,
                        session_location=rooms[(session_id_counter) % len(rooms)],
                        session_date=session_date,
                        start_time=time(start_h, 0),
                        end_time=time(start_h + 2, 0)
                    )
                    sessions.append(session)
                    session_id_counter += 1
        db.add_all(sessions)
        db.commit()

        # 8) Student attendance (StudentSession) - random attendance
        student_sessions = []
        for session in sessions:
            # Get students from the course that has this session's module
            module_id = session.module_id
            course_has_module = None
            for course in courses:
                if any(m.module_id == module_id for m in course.modules):
                    course_has_module = course
                    break
            if course_has_module:
                course_students = [s for s in students if s.course_id == course_has_module.course_id]
                for student in course_students[:len(course_students)]:
                    attendance = (session.session_id + student.student_id) % 10 > 2  # 70% attendance
                    st_sess = StudentSession(student_id=student.student_id, session_id=session.session_id, status=attendance)
                    student_sessions.append(st_sess)
        db.add_all(student_sessions)
        db.commit()

        # 9) Assignments - 40 assignments, multiple per module
        assignments = []
        for module in modules:
            for week in range(1, 5):  # 4 assignments per module
                due_day = 7 + week * 7
                if due_day > 30:
                    due_month = 12
                    due_day -= 30
                else:
                    due_month = 11
                assignment = Assignment(
                    module_id=module.module_id,
                    assignment_name=f"{module.module_name} Assignment {week}",
                    due_date=date(2025, due_month, due_day)
                )
                assignments.append(assignment)
        db.add_all(assignments)
        db.commit()

        # 10) Student assignments with grades - all students submit all assignments
        student_assignments = []
        for assignment in assignments:
            # Find module and get course
            module = db.query(Module).filter(Module.module_id == assignment.module_id).first()
            course_has_module = None
            for course in courses:
                if any(m.module_id == module.module_id for m in course.modules):
                    course_has_module = course
                    break
            if course_has_module:
                course_students = [s for s in students if s.course_id == course_has_module.course_id]
                for i, student in enumerate(course_students):
                    # Random submission date before due date
                    days_before = 1 + (i % 7)
                    submit_date = assignment.due_date - __import__('datetime').timedelta(days=days_before)
                    grade = 40 + (assignment.assignment_id * 13 + student.student_id * 7) % 60  # 40-100
                    sa = StudentAssignment(
                        student_id=student.student_id,
                        assignment_id=assignment.assignment_id,
                        submitted_date=datetime(submit_date.year, submit_date.month, submit_date.day, 10 + i % 12, 0),
                        grade=float(grade)
                    )
                    student_assignments.append(sa)
        db.add_all(student_assignments)
        db.commit()

        # Print counts for verification
        counts = {
            "courses": db.query(Course).count(),
            "modules": db.query(Module).count(),
            "users": db.query(UserAccount).count(),
            "audit_logins": db.query(AuditLogin).count(),
            "students": db.query(Student).count(),
            "wellbeing": db.query(Wellbeing).count(),
            "sessions": db.query(Session).count(),
            "student_sessions": db.query(StudentSession).count(),
            "assignments": db.query(Assignment).count(),
            "student_assignments": db.query(StudentAssignment).count(),
        }

        print("\n" + "="*50)
        print("Database seeding complete!")
        print("="*50)
        for k, v in counts.items():
            print(f" - {k}: {v}")
        print("="*50 + "\n")

    finally:
        db.close()


if __name__ == "__main__":
    import sys
    reset_flag = "--reset" in sys.argv or "--force" in sys.argv
    seed(reset=reset_flag)
