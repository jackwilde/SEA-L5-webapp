import re


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

print(check_password_strength("password"))