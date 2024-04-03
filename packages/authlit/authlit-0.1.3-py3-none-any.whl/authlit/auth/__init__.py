import os, json, yaml
from argon2 import PasswordHasher

ph = PasswordHasher()


def check_json_auth_file(filename) -> list:
    """
    Checks if the auth file (where the user info is stored) already exists.
    """
    path = os.getcwd()
    if os.path.exists(f"{path}/{filename}"):
        with open(f"{path}/{filename}", "r") as f:
            return json.load(f)
    else:
        with open(f"{path}/{filename}", "w") as f:
            json.dump([], f)
        return []
    

def check_yaml_auth_file(filename) -> list:
    """
    Checks if the auth file (where the user info is stored) already exists.
    """
    path = os.getcwd()
    if os.path.exists(f"{path}/{filename}"):
        with open(f"{path}/{filename}", "r") as f:
            return yaml.safe_load(f)
    else:
        with open(f"{path}/{filename}", "w") as f:
            yaml.safe_dump([], f)
        return []


