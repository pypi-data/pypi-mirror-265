import os

SQL_AUTH = os.getenv("SQL_AUTH", False)
MONGO_AUTH = os.getenv("MONGO_AUTH", False)
JSON_AUTH = os.getenv("JSON_AUTH", False)
YAML_AUTH = os.getenv("YAML_AUTH", False)

USE_SQLLITE = os.getenv("USE_SQLLITE", False)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")

JSON_FILE = os.getenv("JSON_FILE", "users.json")

YAML_FILE = os.getenv("YAML_FILE", "users.yaml")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME")