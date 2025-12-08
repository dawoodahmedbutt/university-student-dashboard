from src.Domain_Layer.Entities.StudentSession import StudentSession


def test_studentsession_attributes():
    ss = StudentSession(student_id=3, session_id=4, status=True)
    assert ss.student_id == 3
    assert ss.session_id == 4
    assert ss.status is True
