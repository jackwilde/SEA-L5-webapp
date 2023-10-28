from sqlalchemy import Column, Integer, String, Text

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    password = Column(Text)
    role = Column(String(20))
