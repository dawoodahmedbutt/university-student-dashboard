from Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from Domain_Layer.I_Repositories.IAuditLogRepo import IAuditLogRepo
from Domain_Layer.Entities.AuditLog import AuditLog

class AuditLogRepo(BaseRepo[AuditLog], IAuditLogRepo):

    def __init__(self, session):
        super().__init__(session, AuditLog)
    