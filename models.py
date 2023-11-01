from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    password = Column(Text)
    role = Column(String(20))

    def __repr__(self):
        return f"user_id: {self.id}, email={self.email}"

    def __init__(self, first_name, last_name,
                 email, password, role="standard"):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.role = role