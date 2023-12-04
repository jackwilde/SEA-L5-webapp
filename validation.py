import re
from werkzeug.security import check_password_hash
from datetime import date, datetime
import crud


def validate_email(email):
    email_match_pattern = r"^\S+@\S+\.\S+$"
    if re.match(email_match_pattern, email):
        return True
    else:
        return False


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
    if not check_string:
        return "empty"
    elif re.match(start_end_spaces_pattern, check_string):
        return "contains invalid whitespace"
    else:
        return None


def check_name(name):
    result = check_invalid_spaces(name)
    if result:
        return result
    else:
        # Check name only contains alpha characters and spaces
        name_regex = r"^[a-zA-Z\s]*$"
        if not re.match(name_regex, name):
            return None
        else:
            return "contains invalid characters"


def validate_sign_up(first_name, last_name, email, password1, password2):
    """Will return an error message if an error is found else
    returns None"""
    message = None
    # Check if user exists and then validate input
    user = crud.get_user_by_email(email=email)
    if user:
        message = f"Account already exists for {email}"
    elif not check_name(first_name):
        message = "First name is invalid"
    elif not last_name:
        message = "Last name is invalid"
    elif not validate_email(email):
        message = "Email address format is invalid"
    elif password1 != password2:
        message = "Passwords do not match"
    elif not check_password_strength(password1):
        message = \
            ("Passwords must be at least 8 characters long and contain at "
             "least 1 letter, 1 number, 1 special character and no spaces.")

    if message:
        return message
    else:
        return None


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
