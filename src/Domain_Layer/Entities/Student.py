class Student:
    def __init__(self, student_id, first_name, last_name, address, course_id, year_of_study, email):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.course_id = course_id
        self.year_of_study = year_of_study
        self.email = email
        self.sessions = []
        self.assignments = []


    def add_session(self, session):
     self.sessions.append(session)


    def add_assignment(self, assignment):
     self.assignments.append(assignment)