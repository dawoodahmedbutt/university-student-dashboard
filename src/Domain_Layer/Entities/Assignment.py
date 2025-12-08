class Assignment:
    def __init__(self, assignment_id, module_id, assignment_name, due_date):
        self.assignment_id = assignment_id
        self.module_id = module_id
        self.assignment_name = assignment_name
        self.due_date = due_date
        self.students = []


    def add_student(self, student):
        self.students.append(student)