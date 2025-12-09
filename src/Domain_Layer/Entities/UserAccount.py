class UserAccount:
    def __init__(self, password, username, role):
        self.password = password
        self.username = username
        self.role = role
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)
