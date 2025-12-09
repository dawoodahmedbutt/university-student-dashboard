from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IWellbeingRepo import IWellbeingRepo
from src.Data_Access_Layer.Tables.Wellbeing import Wellbeing as WellbeingTable
from src.Domain_Layer.Entities.Wellbeing import Wellbeing as WellbeingEntity
from sqlalchemy.exc import IntegrityError

class WellbeingRepo(BaseRepo[WellbeingEntity], IWellbeingRepo):

    def __init__(self, session):
        super().__init__(session, WellbeingTable)

    def _to_entity(self, orm):
        wellbeing = WellbeingEntity(
            orm.wellbeing_id,
            orm.student_id,
            orm.date,
            orm.stress_level,
            orm.activity_level,
            orm.quality_of_food,
            orm.alcohol_drug_consumption,  
            orm.medication,
            orm.hours_slept,
        )
        return wellbeing
    
    def _to_orm(self, entity):
        wellbeing_orm = WellbeingTable(
            wellbeing_id=entity.wellbeing_id,
            student_id=entity.student_id,
            date=entity.date,
            stress_level=entity.stress_level,
            activity_level=entity.activity_level,
            quality_of_food=entity.quality_of_food,
            alcohol_drug_consumption=entity.alcohol_drug_consumption,
            medication=entity.medication,
            hours_slept=entity.hours_slept
        )
        return wellbeing_orm
    
    def add(self, entity) -> WellbeingEntity:
        try:
            # Try to add normally
            orm = self._to_orm(entity)
            self.session.add(orm)
            self.session.commit()
            self.session.refresh(orm)
            return self._to_entity(orm)
        except IntegrityError as e:
            # If unique constraint violation, find and update existing record
            self.session.rollback()
            if 'unique_student_date' in str(e).lower() or 'unique' in str(e).lower():
                existing = (
                    self.session.query(WellbeingTable)
                    .filter(
                        WellbeingTable.student_id == entity.student_id,
                        WellbeingTable.date == entity.date
                    )
                    .first()
                )
                if existing:
                    # Update existing record
                    existing.stress_level = entity.stress_level
                    existing.activity_level = entity.activity_level
                    existing.quality_of_food = entity.quality_of_food
                    existing.alcohol_drug_consumption = entity.alcohol_drug_consumption
                    existing.medication = entity.medication
                    existing.hours_slept = entity.hours_slept
                    self.session.commit()
                    self.session.refresh(existing)
                    return self._to_entity(existing)
            # If it's a different integrity error, re-raise
            raise
    
    def get_all_by_studentIDs(self, student_ids: list):
        rows = (
            self.session.query(WellbeingTable)
            .filter(WellbeingTable.student_id.in_(student_ids))
            .all()
        )
        return [self._to_entity(r) for r in rows]
