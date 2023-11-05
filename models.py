from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    password = Column(Text, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id: {self.id}, email={self.email}"

    def __init__(self, first_name, last_name,
                 email, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class Training(Base):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    course_name = Column(String(120), nullable=False)
    course_category = Column(String(60), nullable=False)
    date_completed = Column(Date, nullable=False)
    certification = Column(Boolean)
