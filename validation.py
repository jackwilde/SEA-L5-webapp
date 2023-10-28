# from pydantic import BaseModel, EmailStr, SecretStr
import re

# class SignUp(BaseModel):
#
#     first_name: str
#     last_name: str
#     email: EmailStr
#     password1: SecretStr
#     password2: SecretStr


def validate_sign_up(first_name, last_name, email, password1, password2):
    """Will return an error message if an error is found else
    returns None"""
    message = None

    # if user:
    #     flash(message=f"Account already exists for {email}",
    #           category="error")
    if not first_name:
        message = "First name is required"
    elif not last_name:
        message = "Last name is required"
    elif not validate_email(email):
        message = "Email address format is invalid"
    elif password1 != password2:
        message = "Passwords do not match"
    elif not check_password_strength(password1):
        message = "Passwords must be at least 12 characters long and contain at least 1 letter, 1 number, 1 special character and no spaces."

    if message:
        return message
    else:
        return None


def validate_email(email):
    email_match_pattern = r"^\S+@\S+\.\S+$"
    if re.match(email_match_pattern, email):
        return True
    else:
        return False

def check_password_strength(password):
    password_match_pattern = r"^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[^a-zA-Z\d\s]).{12,}$"
    if re.match(password_match_pattern, password):
        return True
    else:
        return False

