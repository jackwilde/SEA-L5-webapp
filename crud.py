from werkzeug.security import generate_password_hash
from models import User
from database import db


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def create_user(first_name, last_name, email, password):
    password_hash = generate_password_hash(password, method="sha256")
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password_hash)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user
