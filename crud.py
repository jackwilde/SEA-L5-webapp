from sqlalchemy import select, update, delete
from werkzeug.security import generate_password_hash
from models import User, Training, TrainingCategory
from database import Session
from os import getenv


def get_user_by_email(email):
    with Session() as s:
        stmt = select(User).where(User.email == email)
        user = s.execute(stmt).first()
        if user:
            return user[0]


def get_user_by_id(user_id):
    with Session() as s:
        stmt = select(User).where(User.id == user_id)
        user = s.execute(stmt).first()
        if user:
            return user[0]


def get_all_users():
    with Session() as s:
        stmt = select(User.id,
                      User.first_name,
                      User.last_name,
                      User.email,
                      User.admin).order_by(User.id)
        all_users = s.execute(stmt).all()

    return all_users


def create_user(first_name, last_name, email, password, admin=False):
    if admin == "True" or admin is True:
        admin = True
    else:
        admin = False
    password_hash = generate_password_hash(password, method="scrypt")
    with Session() as s:
        user = User(first_name=first_name, last_name=last_name,
                    email=email, password=password_hash, admin=admin)
        s.add(user)
        s.commit()
        s.refresh(user)
    return user


def update_user(user_id, first_name, last_name, email, admin,):
    if admin == "True" or admin is True:
        admin = True
    else:
        admin = False
    s = Session()
    stmt = (update(User)
            .where(User.id == user_id)
            .values(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    admin=admin))
    s.execute(stmt)
    s.commit()
    s.close()
    return 0


def delete_user(user_id):
    # First delete user's training records
    with Session() as s:
        stmt = delete(Training).where(Training.user_id == user_id)
        s.execute(stmt)
        s.commit()
    # Finally delete user
    with Session() as s:
        stmt = delete(User).where(User.id == user_id)
        s.execute(stmt)
        s.commit()
    return 0


def get_training_categories():
    with Session() as s:
        stmt = select(
            TrainingCategory.id, TrainingCategory.category_name
        ).order_by(TrainingCategory.category_name)
        training_categories = s.execute(stmt).all()
    return training_categories


def get_training_category(category_id):
    with (Session() as s):
        stmt = select(
            TrainingCategory.id,
            TrainingCategory.category_name
        ).where(TrainingCategory.id == category_id)
        training_category = s.execute(stmt).first()
    return training_category


def get_training_by_category(category_id):
    with Session() as s:
        stmt = (
            select(
                Training.id,
                User.id,
                User.first_name,
                User.last_name,
                Training.course_name,
                Training.category_id,
                TrainingCategory.category_name,
                Training.date_completed,
                Training.certification
            ).join(TrainingCategory)
            .join(User)
            .where(Training.category_id == category_id)
            .order_by(Training.user_id)
            .order_by(Training.course_name)
        )
        all_training = s.execute(stmt).all()

    return all_training


def create_training_category(training_category):
    with Session() as s:
        training_category = TrainingCategory(category_name=training_category)
        s.add(training_category)
        s.commit()
        s.refresh(training_category)
    return 0


def get_all_training():
    with Session() as s:
        stmt = (
            select(
                Training.id,
                User.id,
                User.first_name,
                User.last_name,
                Training.course_name,
                Training.category_id,
                TrainingCategory.category_name,
                Training.date_completed,
                Training.certification
            ).join(TrainingCategory)
            .join(User)
            .order_by(Training.user_id)
            .order_by(Training.course_name)
        )
        all_training = s.execute(stmt).all()

    return all_training


def get_training_by_id(training_id):
    with Session() as s:
        stmt = select(Training).where(Training.id == training_id)
        training = s.execute(stmt).first()
        if training:
            return training[0]


def get_training_by_user(user):
    with Session() as s:
        stmt = (
            select(
                Training.id,
                Training.course_name,
                Training.category_id,
                TrainingCategory.category_name,
                Training.date_completed,
                Training.certification
            ).join(TrainingCategory)
            .where(Training.user_id == user.id)
            .order_by(Training.date_completed)
            )
        user_training = s.execute(stmt).all()

    return user_training


def create_training(user_id, course_name, course_category, date_completed,
                    certification):
    if certification == "True" or certification is True:
        certification = True
    else:
        certification = False
    with Session() as s:
        training = Training(user_id=user_id,
                            course_name=course_name,
                            category_id=course_category,
                            date_completed=date_completed,
                            certification=certification)
        s.add(training)
        s.commit()
        s.refresh(training)
    return 0


def update_training(training_id, course_name, course_category,
                    date_completed, certification):
    if certification == "True" or certification is True:
        certification = True
    else:
        certification = False
    with Session() as s:
        stmt = (update(Training)
                .where(Training.id == training_id)
                .values(course_name=course_name,
                        category_id=course_category,
                        date_completed=date_completed,
                        certification=certification))
        s.execute(stmt)
        s.commit()
    return 0


# If no users create first admin
if not get_all_users():
    create_user(
        first_name=getenv("ADMIN_FIRST_NAME"),
        last_name=getenv("ADMIN_LAST_NAME"),
        email=getenv("ADMIN_EMAIL"),
        password=getenv("ADMIN_PASSWORD"),
        admin=True
    )


# If no training categories then create them
if not get_training_categories():
    category_list = [
        "Cloud Computing",
        "Cyber Security",
        "Data Management",
        "Development",
        "Networking",
        "Project Management"
    ]
    for category in category_list:
        create_training_category(category)

# Get all categories
ALL_CATEGORIES = get_training_categories()
