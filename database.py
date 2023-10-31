from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


DB_NAME = "data.db"
DB_PATH = f"{Path(__file__).parent}/{DB_NAME}"
db = SQLAlchemy()

# Create database
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
