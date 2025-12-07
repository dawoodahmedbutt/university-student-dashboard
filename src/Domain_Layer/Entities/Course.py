class Course:
    def __init__(self, course_id, course_name, course_director, education_level):
        self.course_id = course_id
        self.course_name = course_name
        self.course_director = course_director
        self.education_level = education_level
        self.modules = []


    def add_module(self, module):
        self.modules.append(module)