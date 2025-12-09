from abc import ABC
from Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from Domain_Layer.Entities.AuditLog import AuditLog

class IAuditLogtRepo(IBaseRepo[AuditLog], ABC):
    pass
