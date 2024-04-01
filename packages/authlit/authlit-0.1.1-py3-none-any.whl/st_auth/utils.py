import re, secrets
import time, random
import streamlit as st
from authlit.auth import mongo_auth as ma
from authlit.auth import sql_auth as sa
from authlit.auth import json_auth as ja
from authlit.auth import yaml_auth as ya
from authlit.config import MONGO_AUTH, SQL_AUTH, JSON_AUTH, YAML_AUTH


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticates the username and password against the database.
    """
    if SQL_AUTH:
        return sa.authenticate_with_sql(username, password)
    elif MONGO_AUTH:
        return ma.authenticate_with_mongo(username, password)
    elif JSON_AUTH:
        return ja.authenticate_with_json(username, password)
    elif YAML_AUTH:
        return ya.authenticate_with_yaml(username, password)
    else:
        raise ValueError("No authentication method is enabled. Please enable one.")


def is_valid_username(username: str) -> bool:
    """
    Checks if the username is valid.
    """
    username_regex = r"^[A-Za-z_][A-Za-z0-9_]*$"
    return bool(re.match(username_regex, username))


def is_email_valid(email: str) -> bool:
    """
    Validates the provided email.
    """
    email_regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    return bool(re.fullmatch(email_regex, email))


def generate_random_passwd() -> str:
    """
    Generates a random password.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def is_email_unique(email):
    if SQL_AUTH:
        return sa.is_email_unique(email)
    elif MONGO_AUTH:
        return ma.is_email_unique(email)
    elif JSON_AUTH:
        return ja.is_email_unique(email)
    elif YAML_AUTH:
        return ya.is_email_unique(email)


def is_username_unique(username):
    if SQL_AUTH:
        return sa.is_username_unique(username)
    elif MONGO_AUTH:
        return ma.is_username_unique(username)
    elif JSON_AUTH:
        return ja.is_username_unique(username)
    elif YAML_AUTH:
        return ya.is_username_unique(username)


def register_user(name, email, username, password):
    if SQL_AUTH:
        sa.register_user(name, email, username, password)
    elif MONGO_AUTH:
        ma.register_user(name, email, username, password)
    elif JSON_AUTH:
        ja.register_user(name, email, username, password)
    elif YAML_AUTH:
        ya.register_user(name, email, username, password)


def update_password(password, email=None, username=None):
    if SQL_AUTH:
        username = sa.is_email_present(email).username or username
        sa.update_password(username, password)
    elif MONGO_AUTH:
        user = ma.is_email_present(email)
        username = user.get("username") or username
        ma.update_password(username, password)
    elif JSON_AUTH:
        ja.update_password(username, email, password)
    elif YAML_AUTH:
        ya.update_password(username, email, password)
    return username


# Function to generate OTP
def generate_otp(expiry_time):
    otp = random.randint(100000, 999999)
    st.session_state.otp = {"value": otp, "expiry_time": time.time() + expiry_time}
    return otp

# Function to retrieve stored OTP securely
def get_otp():
    if "otp" in st.session_state:
        if time.time() < st.session_state.otp["expiry_time"]:
            return st.session_state.otp["value"]
    return None

