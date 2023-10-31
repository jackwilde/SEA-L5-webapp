from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

db = SQLAlchemy()

# Create database
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
