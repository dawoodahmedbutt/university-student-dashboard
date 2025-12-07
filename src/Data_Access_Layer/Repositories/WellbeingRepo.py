from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IWellbeingRepo import IWellbeingRepo
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing as WellbeingTable
from src.Domain_Layer.Entities.Wellbeing import Wellbeing as WellbeingEntity


class WellbeingRepo(BaseRepo[WellbeingEntity], IWellbeingRepo):

    def __init__(self, session):
        super().__init__(session, WellbeingTable)

    def _to_entity(self, row: WellbeingTable) -> WellbeingEntity:
        return WellbeingEntity(
            row.wellbeing_id,
            row.student_id,
            row.date,
            row.stress_level,
            row.activity_level,
            row.quality_of_food,
            row.alcohol_drug_consumption,
            row.medication,
            row.hours_slept,
        )

    def _to_orm(self, entity: WellbeingEntity) -> WellbeingTable:
        return WellbeingTable(
            wellbeing_id=getattr(entity, "wellbeing_id", None),
            student_id=entity.student_id,
            date=entity.date,
            stress_level=getattr(entity, "stress_level", getattr(entity, "stress", None)),
            activity_level=getattr(entity, "activity_level", getattr(entity, "activity", None)),
            quality_of_food=getattr(entity, "quality_of_food", getattr(entity, "food_quality", None)),
            alcohol_drug_consumption=getattr(entity, "alcohol_drug_consumption", getattr(entity, "alcohol_drugs", None)),
            medication=entity.medication,
            hours_slept=entity.hours_slept,
        )
