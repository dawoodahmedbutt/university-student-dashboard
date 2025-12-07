class Session:
    def __init__(self,session_id, module_id, session_location, start_time, end_time, session_date):
        if end_time <= start_time:
            raise ValueError("Session end time must be after start time.")

        if module_id is None:
            raise ValueError("Module is required")
        self.session_id = session_id
        self.module_id = module_id
        self.session_location = session_location
        self.start_time = start_time
        self.end_time = end_time
        self.session_date = session_date
        self.students = []

    def add_student(self, student):
        if student in self.students:
            raise ValueError("Student already registered in this session.")
        self.students.append(student)