from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IUserAccountRepo import IUserAccountRepo
from src.Domain_Layer.Entities.UserAccount import UserAccount as UserAccountEntity
from src.Data_Access_Layer.Tables.UserAccount import UserAccount as UserAccountTable


class UserAccountRepo(BaseRepo[UserAccountEntity], IUserAccountRepo):

    def __init__(self, session):
        super().__init__(session, UserAccountTable)

    def _to_entity(self, row: UserAccountTable) -> UserAccountEntity:
        return UserAccountEntity(row.user_id, row.email, row.password, row.role)

    def _to_orm(self, entity: UserAccountEntity) -> UserAccountTable:
        return UserAccountTable(user_id=getattr(entity, "user_id", None), email=entity.email, password=entity.password, role=entity.role)
