from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
import models


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: models.User):
    password_hash = generate_password_hash(user.password, method="scrypt")
    db_user = models.User(first_name=user.first_name, last_name=user.last_name,
                          email=user.email, password=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
