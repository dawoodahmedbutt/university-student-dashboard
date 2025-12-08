class StudentSession:
    def __init__(self, student_id: int, session_id: int, status: bool):
        """
        Represents the attendance of a student in a particular session.

        :param student_id: ID of the student
        :param session_id: ID of the session
        :param status: Attendance status (e.g., "present (1)", "absent (0)")
        """
        self.student_id = student_id
        self.session_id = session_id
        self.status = status


