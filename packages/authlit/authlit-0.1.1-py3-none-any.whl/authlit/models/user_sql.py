from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))

    def __repr__(self):
        return f"<User(username='{self.username}', name='{self.name}', email='{self.email}')>"
