class User:
    def __init__(self, username):
        self._username = username
        self._email = ""
        self._full_name = ""

    def __str__(self):
        return self.username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def email(self):
        return self._username

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def full_name(self):
        return self._username

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name
        }