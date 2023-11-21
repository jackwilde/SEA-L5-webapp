from sqlalchemy.orm import load_only
from sqlalchemy import select, update
from werkzeug.security import generate_password_hash
from models import User, Training, TrainingCategory
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
    password_hash = generate_password_hash(password, method="scrypt")
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password_hash)
    s.add(user)
    s.commit()
    s.refresh(user)
    s.close()
    return user


def get_training_categories():
    s = Session()
    training_categories = (s.query(TrainingCategory).all())
    return training_categories


def get_training_by_user(user):
    with Session() as s:
        print(user.id)
        s.add(user)
        stmt = (
            select(Training.id,
                   Training.course_name,
                   Training.category_id,
                   TrainingCategory.category_name,
                   Training.date_completed,
                   Training.certification
            )
            .join(TrainingCategory)
            .where(Training.user_id == user.id)
            .order_by(Training.date_completed)
        )
        user_training = s.execute(stmt).all()

    return user_training


def create_training(user_id, course_name, course_category, date_completed,
                    certification):
    s = Session()
    training = Training(user_id=user_id,
                        course_name=course_name,
                        category_id=course_category,
                        date_completed=date_completed,
                        certification=certification)
    s.add(training)
    s.commit()
    s.refresh(training)
    s.close()
    return 0


def update_training(training_id, user_id, course_name, course_category,
                    date_completed, certification):
    s = Session()
    stmt = (update(Training)
            .where(Training.id == training_id)
            .values(user_id=user_id,
                    course_name=course_name,
                    category_id=course_category,
                    date_completed=date_completed,
                    certification=certification))
    s.execute(stmt)
    s.commit()
    s.close()
    return 0