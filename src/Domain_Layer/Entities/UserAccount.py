class UserAccount:
    def __init__(self, user_id, email, password, role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)
