from sqlalchemy import select, update, delete
from werkzeug.security import generate_password_hash
from models import User, Training, TrainingCategory
from database import Session
from os import getenv


def get_user_by_email(email: str):
    """
    Search for user by email address.
    :param email: Email address to search for
    :return: User (If present)
    """
    with Session() as s:
        stmt = select(User).where(User.email == email)
        user = s.execute(stmt).first()
        if user:
            return user[0]


def get_user_by_id(user_id: int):
    """
    Search for user by user id.
    :param user_id: User id to search for
    :return: User (If present)
    """
    with Session() as s:
        stmt = select(User).where(User.id == user_id)
        user = s.execute(stmt).first()
        if user:
            return user[0]


def get_all_users():
    """
    Get all users in the database.
    :return: List of User objects
    """
    with Session() as s:
        stmt = select(User.id,
                      User.first_name,
                      User.last_name,
                      User.email,
                      User.admin).order_by(User.id)
        all_users = s.execute(stmt).all()

    return all_users


def create_user(first_name, last_name, email, password, admin):
    """
    Add a new user in the database.
    :param first_name: User's first name
    :param last_name: User's last name
    :param email: User's email address
    :param password: User's password
    :param admin: User is admin True/False
    :return: Created User object
    """
    # Ensure admin value is bool
    if admin == "True" or admin is True:
        admin = True
    else:
        admin = False
    password_hash = generate_password_hash(password, method="scrypt")
    with Session() as s:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password_hash,
            admin=admin
        )
        s.add(user)
        s.commit()
        s.refresh(user)
    return user


def update_user(user_id, first_name, last_name, email, admin,):
    """
    Update existing user details in database.
    :param user_id: ID of user to update
    :param first_name: User's new first name
    :param last_name: User's new last name
    :param email: User's new email address
    :param admin: User's new admin status True/False
    :return: 0 on success
    """
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
    """
    Delete user from database.
    :param user_id: ID of user to be deleted
    :return: 0 on success
    """
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
    """
    Get all training categories from database.
    :return: List of TrainingCategory objects
    """
    with Session() as s:
        stmt = select(
            TrainingCategory.id, TrainingCategory.category_name
        ).order_by(TrainingCategory.category_name)
        training_categories = s.execute(stmt).all()
    return training_categories


def get_training_category(category_id):
    """
    Get training category by ID.
    :param category_id: ID of category to search.
    :return: TrainingCategory object
    """
    with (Session() as s):
        stmt = select(
            TrainingCategory.id,
            TrainingCategory.category_name
        ).where(TrainingCategory.id == category_id)
        training_category = s.execute(stmt).first()
    return training_category


def get_training_by_category(category_id):
    """
    Get all training within a category.
    :param category_id: ID of training category to search
    :return: List of training records within category
    """
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
    """
    Create a new training category.
    :param training_category: New training category name
    :return: 0 on success
    """
    with Session() as s:
        training_category = TrainingCategory(category_name=training_category)
        s.add(training_category)
        s.commit()
        s.refresh(training_category)
    return 0


def get_all_training():
    """
    Get all training records in database.
    :return: list of all training records
    """
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
    """
    Get training record by ID.
    :param training_id: ID of training to search
    :return: Training object if found
    """
    with Session() as s:
        stmt = select(Training).where(Training.id == training_id)
        training = s.execute(stmt).first()
        if training:
            return training[0]


def get_training_by_user(user):
    """
    Get training from User object.
    :param user: User object to search
    :return: List of training records for user
    """
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
        training = Training(
            user_id=user_id,
            course_name=course_name,
            category_id=course_category,
            date_completed=date_completed,
            certification=certification
        )
        s.add(training)
        s.commit()
        s.refresh(training)
    return 0


def update_training(training_id, course_name, course_category,
                    date_completed, certification):
    """
    Update existing training record in database.
    :param training_id: ID of training record to update
    :param course_name: Updated course name
    :param course_category: Updated course category
    :param date_completed: Updated date completed
    :param certification: Updated certification True/False
    :return: 0 on success
    """
    if certification == "True" or certification is True:
        certification = True
    else:
        certification = False
    with Session() as s:
        stmt = (update(Training)
                .where(Training.id == training_id)
                .values(
                    course_name=course_name,
                    category_id=course_category,
                    date_completed=date_completed,
                    certification=certification
                )
        )
        s.execute(stmt)
        s.commit()
    return 0


def delete_training(training_id):
    """
    Delete training record from database.
    :param training_id: ID of training record to delete
    :return: 0 on success
    """
    with Session() as s:
        stmt = delete(Training).where(Training.id == training_id)
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
