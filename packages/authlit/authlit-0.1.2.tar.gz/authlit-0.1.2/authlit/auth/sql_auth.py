from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from authlit.auth import ph
from authlit.models.user_sql import User, Base
from authlit.config import SQL_AUTH, USE_SQLLITE, DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USERNAME


if SQL_AUTH:
    if USE_SQLLITE:
        engine = create_engine("sqlite:///auth.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
    else:
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
            engine = create_engine(
                f"mysql+pymysql://{username}:{password}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
            )
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)


def authenticate_with_sql(username: str, password: str) -> bool:
    """
    Authenticates the username and password against the database.
    """
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        try:
            return ph.verify(user.password, password)
        except:
            return False
    else:
        return False


def is_email_unique(email: str) -> bool:
    """
    Checks if the email is unique.
    """
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    return not user


def is_username_unique(username: str) -> bool:
    """
    Checks if the username is unique.
    """
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return not user


def register_user(name: str, email: str, username: str, password: str) -> None:
    """
    Saves the information of the new user in the database.
    """
    hashed_password = ph.hash(password)
    new_user = User(name=name, email=email, username=username, password=hashed_password)
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()


def update_password(username: str, password: str) -> None:
    """
    Updates the password of the user.
    """
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    user.password = ph.hash(password)
    session.commit()
    session.close()


def is_email_present(email: str):
    """
    Checks if the email entered is present in the database.
    """
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    return user
