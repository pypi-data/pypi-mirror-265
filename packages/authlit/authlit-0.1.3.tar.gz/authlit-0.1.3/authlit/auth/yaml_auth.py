import yaml
from authlit.models.user import User
from authlit.auth import check_yaml_auth_file
from authlit.auth import ph
from authlit.config import YAML_AUTH, YAML_FILE


class YAMLAuth:
    def __init__(self):
        if YAML_AUTH:
            self.users = check_yaml_auth_file(YAML_FILE)

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
        with open(YAML_FILE, "w") as file:
            yaml.safe_dump(self.users, file)
            

    def update_password(self, username: str, password: str) -> None:
        """
        Updates the password of the user.
        """
        user = User.find_by_username(username, users=self.users)
        user["password"] = ph.hash(password)
        with open(YAML_FILE, "w") as file:
            yaml.safe_dump(self.users, file)


ya = YAMLAuth()

def authenticate_with_yaml(username: str, password: str) -> bool:
    """
    Authenticates the username and password against the database.
    """
    return ya.authenticate_user(username, password)


def is_email_unique(email: str) -> bool:
    """
    Checks if the email is unique.
    """
    return User.find_by_email(email, users=ya.users) is None


def is_username_unique(username: str) -> bool:
    """
    Checks if the username is unique.
    """
    return User.find_by_username(username, users=ya.users) is None


def register_user(name: str, email: str, username: str, password: str) -> None:
    """
    Saves the information of the new user in the database.
    """
    ya.register_user(name, email, username, password)


def update_password(username: str, email: str, password: str) -> None:
    """
    Updates the password of the user.
    """
    if email:
        user = User.find_by_email(email, users=ya.users)
        if user:
            username = user.get("username")
            ya.update_password(username, password)
    else:
        ya.update_password(username, password)