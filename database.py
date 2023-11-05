from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from os import getenv

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")

# Create database
SQLALCHEMY_DATABASE_URL = \
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # Create DB
Base.metadata.create_all(bind=engine, checkfirst=True)
