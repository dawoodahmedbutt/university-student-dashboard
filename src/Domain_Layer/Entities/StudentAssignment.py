class StudentAssignment:
    def __init__(self, student_id: int, assignment_id: int, grade: float, submitted_date ):
        """
        Represents a student's submission for a specific assignment.

        :param student_id: ID of the student
        :param assignment_id: ID of the assignment
        :param status: Submission status (e.g., "submitted", "pending", "late")
        :param grade: Optional grade for the assignment
        """
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.submitted_date = submitted_date
        self.grade = grade


    def add_grade(self, grade: float):
        self.grade = grade

    def add_note(self, note: str):
        self.submission_notes += note + "\n"


