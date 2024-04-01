from urllib.parse import quote_plus
from pymongo import MongoClient
from authlit.models.user_mongo import User
from authlit.config import MONGO_AUTH, DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USERNAME
from authlit.auth import ph
from pymongo.server_api import ServerApi

if MONGO_AUTH:
    if not DB_DATABASE:
        raise ValueError("Please set the environment variable for DB_DATABASE.")
    if not DB_HOST:
        raise ValueError("Please set the environment variable for DB_HOST.")
    if not DB_PASSWORD:
        raise ValueError("Please set the environment variable for DB_PASSWORD.")
    if not DB_PORT:
        raise ValueError("Please set the environment variable for DB_PORT.")
    if not DB_USERNAME:
        raise ValueError("Please set the environment variable for DB_USERNAME.")
    else:
        username = quote_plus(DB_USERNAME)
        password = quote_plus(DB_PASSWORD)
        uri = f"mongodb+srv://{username}:{password}@{DB_HOST}/?retryWrites=true&w=majority&appName={DB_DATABASE}"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client[DB_DATABASE]
        if "users" not in db.list_collection_names():
            db.create_collection("users")


def authenticate_with_mongo(username: str, password: str) -> bool:
    """
    Authenticates the username and password against the database.
    """
    user = User.find_by_username(db.users, username)
    if user:
        try:
            return ph.verify(user["password"], password)
        except:
            return False
    else:
        return False


def is_email_unique(email: str) -> bool:
    """
    Checks if the email is unique.
    """
    return User.find_by_email(db.users, email) is None


def is_username_unique(username: str) -> bool:
    """
    Checks if the username is unique.
    """
    return User.find_by_username(db.users, username) is None


def register_user(name: str, email: str, username: str, password: str) -> None:
    """
    Saves the information of the new user in the database.
    """
    hashed_password = ph.hash(password)
    new_user = User(username=username, name=name, email=email, password=hashed_password)
    new_user.save(users_collection=db.users)


def update_password(username: str, password: str) -> None:
    """
    Updates the password of the user.
    """
    hashed_password = ph.hash(password)
    User.update_password(db.users, username, hashed_password)


def is_email_present(email: str):
    """
    Checks if the email entered is present in the database.
    """
    return User.find_by_email(db.users, email)
