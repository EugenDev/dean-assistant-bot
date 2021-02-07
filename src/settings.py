class DbSettings:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

class TgConnectionSettings:
    def __init__(self, api_key):
        self.api_key = api_key
