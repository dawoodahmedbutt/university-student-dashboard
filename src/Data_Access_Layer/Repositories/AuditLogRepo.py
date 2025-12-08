from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IAuditLogRepo import IAuditLogRepo
from src.Domain_Layer.Entities.AuditLog import AuditLog as AuditLogEntity
from src.Data_Access_Layer.Tables.AuditLogin import AuditLogin as AuditLoginTable


class AuditLogRepo(BaseRepo[AuditLogEntity], IAuditLogRepo):

    def __init__(self, session):
        super().__init__(session, AuditLoginTable)

    def _to_entity(self, row: AuditLoginTable) -> AuditLogEntity:
        return AuditLogEntity(row.log_id, row.user_id, row.timestamp)

    def _to_orm(self, entity: AuditLogEntity) -> AuditLoginTable:
        return AuditLoginTable(log_id=getattr(entity, "log_id", None), user_id=entity.user_id, timestamp=entity.timestamp)
