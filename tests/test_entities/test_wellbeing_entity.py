from datetime import date

from src.Domain_Layer.Entities.Wellbeing import Wellbeing


def test_wellbeing_attributes_assignment():
    w = Wellbeing(
        wellbeing_id=1,
        student_id=2,
        date=date(2024, 1, 1),
        stress=5,
        activity=6,
        food_quality=7,
        alcohol_drugs=1,
        medication=0,
        hours_slept=8,
    )

    assert w.wellbeing_id == 1
    assert w.student_id == 2
    assert w.stress_level == 5
    assert w.activity_level == 6
    assert w.quality_of_food == 7
    assert w.medication == 0
    assert w.hours_slept == 8
