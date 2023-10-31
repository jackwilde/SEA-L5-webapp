from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create database
SQLALCHEMY_DATABASE_URI = f"sqlite:///data.db"