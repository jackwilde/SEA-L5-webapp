from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    password = db.Column(db.Text)
    role = db.Column(db.String(20))

    def __init__(self, first_name, last_name, email, password, role="Standard"):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.role=role

    def __repr__(self):
        return f"{self.email}"
