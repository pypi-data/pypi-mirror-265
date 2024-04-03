from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def save(self):
        pass

    @staticmethod
    @abstractmethod
    def update_password(username, password):
        pass

    @staticmethod
    def find_by_username(username: str, users: list) -> dict:
        """
        Finds a user by username.
        """
        for user in users:
            if user.get("username") == username:
                return user
        return None

    @staticmethod
    def find_by_email(email: str, users: list) -> dict:
        """
        Finds a user by email.
        """
        for user in users:
            if user.get("email") == email:
                return user
        return None
