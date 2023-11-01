from werkzeug.security import generate_password_hash
from models import User
from database import Session


def get_user_by_email(email):
    s = Session()
    user = s.query(User).filter(User.email == email).first()
    s.close()
    return user


def get_user_by_id(user_id):
    s = Session()
    user = s.query(User).filter(User.id == user_id).first()
    s.close()
    return user


def create_user(first_name, last_name, email, password):
    s = Session()
    password_hash = generate_password_hash(password, method="sha256")
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password_hash)
    s.add(user)
    s.commit()
    s.refresh(user)
    s.close()
    return user
