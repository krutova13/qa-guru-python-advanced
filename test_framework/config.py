class Server:
    def __init__(self, env):
        self.service = {
            "feature": "",
            "dev": "http://localhost:8000/api/v1",
            "rc": "",
        }[env]
