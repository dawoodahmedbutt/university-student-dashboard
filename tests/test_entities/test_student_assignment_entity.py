from src.Domain_Layer.Entities.StudentAssignment import StudentAssignment


def test_studentassignment_add_grade_and_note():
    sa = StudentAssignment(student_id=1, assignment_id=2, grade=None, submitted_date=None)
    sa.add_grade(95.0)
    assert sa.grade == 95.0

    # add_note requires submission_notes attribute to exist; initialize then append
    sa.submission_notes = ""
    sa.add_note("Good work")
    assert "Good work" in sa.submission_notes
