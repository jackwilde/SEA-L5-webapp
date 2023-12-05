import re
from werkzeug.security import check_password_hash
from datetime import date, datetime
import crud


def validate_email(email):
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
    password_match_pattern = \
        r"^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[^a-zA-Z\d\s]).{8,}$"
    if re.match(password_match_pattern, password):
        return True
    else:
        return ("Passwords must be at least 8 characters long and contain at "
                "least 1 letter, 1 number, 1 special character and no spaces.")


def check_invalid_spaces(check_string):
    start_end_spaces_pattern = r"^\s|\s$"
    if re.match(start_end_spaces_pattern, check_string):
        return "contains invalid whitespace"
    else:
        return None


def check_name(name):
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
    """Will return an error message if an error is found else
    returns None"""
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
    """Will return an error message if an error is found else
    returns None"""
    result = validate_user_info(first_name, last_name, email)
    if result != 0:
        return result
    if password1 != password2:
        return "Passwords do not match"
    if not check_password_strength(password1):
        return ("Passwords must be at least 8 characters long and contain at "
                "least 1 letter, 1 number, 1 special character and no spaces.")
    # If all validation passes return 0
    return 0


def validate_password(email, password):
    user = crud.get_user_by_email(email=email)
    if user:
        if check_password_hash(user.password, password):
            return user


def convert_to_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        return None


def check_date_is_past(date_to_check):
    if isinstance(date_to_check, str):
        converted_date = datetime.strptime(date_to_check, "%Y-%m-%d").date()
        if converted_date <= date.today():
            return None
        else:
            message = "Date completed cannot be in the future"
            return message
    else:
        message = "Date format is invalid"
        return message
