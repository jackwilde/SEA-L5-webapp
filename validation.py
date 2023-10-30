import re
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
import crud

from werkzeug.security import check_password_hash

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

def validate_sign_up(db: Annotated[Session, Depends(get_db)],
                     first_name, last_name, email, password1, password2):
    """Will return an error message if an error is found else
    returns None"""
    message = None
    # Check if user exists and then validate input
    user = crud.get_user_by_email(db, email=email)
    if user:
        message = f"Account already exists for {email}"
    elif not first_name:
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

def validate_password(db: Annotated[Session, Depends(get_db)],
                     email, password):
    user = crud.get_user_by_email(db, email=email)
    result = {}
    if user:
        if check_password_hash(user.password, password):
            result["status"] = "success"
            result["message"] = "Sign in successful"
        else:
            result["status"] = "error"
            result["message"] = "Incorrect password"
    else:
        result["status"] = "error"
        result["message"] = f"Account does not exist for {email}"

    return result
