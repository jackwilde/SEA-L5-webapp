import re
from werkzeug.security import check_password_hash
from datetime import date, datetime
import crud


def validate_email(email):
    """
    Validate email address.
    :param email: Email address to validate
    :return: None on success else error message
    """
    email_length_limit = 120
    if len(email) > email_length_limit:
        return f"must be {email_length_limit} characters or less"
    error = check_invalid_spaces(email)
    if error:
        return "contains invalid whitespace"
    email_match_pattern = \
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_match_pattern, email):
        return None
    else:
        return "format is invalid"


def check_password_strength(password):
    """
    Check password strength
    :param password: Password to check
    :return: None on success else error message
    """
    password_match_pattern = \
        r"^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[^a-zA-Z\d\s]).{8,}$"
    if re.match(password_match_pattern, password):
        return None
    else:
        return ("Passwords must be at least 8 characters long and contain at "
                "least 1 letter, 1 number, 1 special character and no spaces.")


def check_invalid_spaces(check_string):
    """
    Check for spaces at the start or end of a string.
    :param check_string: String to check
    :return: None on success else error message
    """
    start_end_spaces_pattern = r"^\s|\s$"
    if re.match(start_end_spaces_pattern, check_string):
        return "contains whitespace at start or end"
    else:
        return None


def check_name(name):
    """
    Check user first or last name.
    :param name: Name to check
    :return: None on success else error message
    """
    name_length_limit = 25
    if len(name) > name_length_limit:
        return f"must be {name_length_limit} characters or less"
    error = check_invalid_spaces(name)
    if error:
        return error
    else:
        # Check name only contains alpha characters and spaces
        name_regex = r"^[a-zA-Z\s]*$"
        if not re.match(name_regex, name):
            return "contains invalid characters"
        else:
            return None


def validate_user_info(first_name, last_name, email, user_id=None):
    """
    Validate user info.
    :param first_name: User's first name
    :param last_name: User's last name
    :param email: User's email address
    :param user_id: User's ID
    :return: 0 on success else error message
    """
    # Check if user exists
    user = crud.get_user_by_email(email=email)
    if user:
        # Check if the user found does not match the user id
        if user.id != user_id:
            return f"Account already exists for {email}"
    # Validate first name
    error = check_name(first_name)
    if error:
        return f"First name {error}"
    # Validate last name
    error = check_name(last_name)
    if error:
        return f"Last name {error}"
    # Validate email
    error = validate_email(email)
    if error:
        return f"Email address {error}"
    # If all validation passes return 0
    return 0


def validate_sign_up(first_name, last_name, email, password1, password2):
    """
    Validate user sign up.
    :param first_name: First name
    :param last_name: Last name
    :param email: Email address
    :param password1: Password
    :param password2: Confirm Password
    :return: 0 on success else error string
    """
    result = validate_user_info(first_name, last_name, email)
    if result != 0:
        return result
    if password1 != password2:
        return "Passwords do not match"
    error = check_password_strength(password1)
    if error:
        return error
    # If all validation passes return 0
    return 0


def validate_password(email, password):
    """
    Validate user password matches stored password.
    :param email: User's email address
    :param password: User's password to check against database.
    :return: User object
    """
    user = crud.get_user_by_email(email=email)
    if user:
        if check_password_hash(user.password, password):
            return user


def convert_to_int(value):
    """
    Safely convert a numeric string to an integer.
    :param value: Value to convert
    :return: Value as integer on success
    """
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        return None


def check_date_is_past(date_to_check):
    """
    Check if a date is in the past.
    :param date_to_check: Date to check
    :return: None on success else error message
    """
    if isinstance(date_to_check, str):
        converted_date = datetime.strptime(date_to_check, "%Y-%m-%d").date()
        if converted_date <= date.today():
            return None
        else:
            message = "cannot be in the future"
            return message
    else:
        message = "format is invalid"
        return message


def validate_training(course_name, date_completed):
    """
    Validate training details.
    :param course_name: Name of course
    :param date_completed: Date of completion
    :return: 0 on success else error message
    """
    course_name_limit = 50
    if len(course_name) > course_name_limit:
        return f"Course name must be {course_name_limit} characters or less"
    error = check_invalid_spaces(course_name)
    if error:
        return f"Course name {error}"
    error = check_date_is_past(date_completed)
    if error:
        return f"Date completed {error}"
    return 0
