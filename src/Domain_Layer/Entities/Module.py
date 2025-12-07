class Module:
    def __init__(self, module_id, module_name, credits, module_leader):
        self.module_id = module_id
        self.module_name = module_name
        self.credits = credits
        self.module_leader = module_leader
        self.courses = []
        self.assignments = []
        self.sessions = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def add_session(self, session):
        self.sessions.append(session)
