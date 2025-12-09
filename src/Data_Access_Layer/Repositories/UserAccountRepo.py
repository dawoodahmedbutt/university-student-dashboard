from src.Data_Access_Layer.Repositories.BaseRepo import BaseRepo
from src.Domain_Layer.I_Repositories.IUserAccountRepo import IUserAccountRepo
from src.Domain_Layer.Entities.UserAccount import UserAccount as UserAccountEntity
from src.Data_Access_Layer.Tables.UserAccount import UserAccount as UserAccountTable

class UserAccountRepo(BaseRepo[UserAccountEntity], IUserAccountRepo):

    def __init__(self, session):
        super().__init__(session, UserAccountTable)

    def _to_entity(self, orm):
        user_account = UserAccountEntity(
            username=orm.email,
            password=orm.password,
            role=orm.role,
        )
        return user_account

    def get_by_username(self, username: str):
        row = (
            self.session.query(UserAccountTable)
            .filter(UserAccountTable.email == username)
            .first()
        )
        if row:
            return self._to_entity(row)
        return None