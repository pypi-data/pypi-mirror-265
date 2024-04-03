import json
from authlit.models.user import User
from authlit.auth import check_json_auth_file
from authlit.auth import ph
from authlit.config import JSON_AUTH, JSON_FILE


class JSONAuth:
    def __init__(self):
        if JSON_AUTH:
            self.users = check_json_auth_file(JSON_FILE)

    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticates the username and password against the database.
        """
        user = User.find_by_username(username, users=self.users)
        if user:
            try:
                return ph.verify(user["password"], password)
            except:
                return False
        else:
            return False

    def is_email_unique(self, email: str) -> bool:
        """
        Checks if the email is unique.
        """
        return User.find_by_email(email, users=self.users) is None

    def is_username_unique(self, username: str) -> bool:
        """
        Checks if the username is unique.
        """
        return User.find_by_username(username, users=self.users) is None

    def register_user(
        self, name: str, email: str, username: str, password: str
    ) -> None:
        """
        Saves the information of the new user in the database.
        """
        hashed_password = ph.hash(password)
        new_user = {
            "name": name,
            "email": email,
            "username": username,
            "password": hashed_password,
        }
        self.users.append(new_user)
        with open(JSON_FILE, "w") as f:
            json.dump(self.users, f, indent=4)

    def update_password(self, username: str, password: str) -> None:
        """
        Updates the password of the user.
        """
        user = User.find_by_username(username, users=self.users)
        user["password"] = ph.hash(password)
        with open(JSON_FILE, "w") as f:
            json.dump(self.users, f, indent=4)


ja = JSONAuth()


def authenticate_with_json(username: str, password: str) -> bool:
    """
    Authenticates the username and password against the database.
    """
    return ja.authenticate_user(username, password)


def is_email_unique(email: str) -> bool:
    """
    Checks if the email is unique.
    """
    return User.find_by_email(email, users=ja.users) is None


def is_username_unique(username: str) -> bool:
    """
    Checks if the username is unique.
    """
    return User.find_by_username(username, users=ja.users) is None


def register_user(name: str, email: str, username: str, password: str) -> None:
    """
    Saves the information of the new user in the json file.
    """
    ja.register_user(name, email, username, password)


def update_password(username: str, email: str, password: str) -> None:
    """
    Updates the password of the user.
    """
    if email:
        user = User.find_by_email(email, users=ja.users)
        if user:
            username = user.get("username")
            ja.update_password(username, password)
    else:
        ja.update_password(username, password)