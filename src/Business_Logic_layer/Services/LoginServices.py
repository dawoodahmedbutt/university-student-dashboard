from src.Data_Access_Layer.Repositories.UserAccountRepo import UserAccountRepo


class LoginServices:
    def __init__(self, db):
        self.repo = UserAccountRepo(db)

    def log_in(self, loginDTO):
        user = self.repo.get_by_username(loginDTO.username)
        if user is not None and user.password == loginDTO.password:
            return {"success": True, "user": user, "role": user.role}
        else:
            return {"success": False, "message": "Invalid username or password."}
