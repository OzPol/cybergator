class User:
    """Defines the User model"""
    def __init__(self, id=None, username="", password=""):
        self.id = id
        self.username = username
        self.password = password

    def to_dict(self):
        """Converts User object to dictionary"""
        return {"id": self.id, "username": self.username, "password": self.password}