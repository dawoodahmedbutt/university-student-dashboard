from src.Data_Access_Layer.Repositories.AssignmentRepo import AssignmentRepo
from datetime import date, time

class AssignmanetServices:
    def __init__(self, db):
        self.repo = AssignmentRepo(db)

    def get_all(self):
        res = self.repo.get_all()
        return res      
        