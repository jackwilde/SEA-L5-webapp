import re


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
        if re.match(name_regex, name):
            return None
        else:
            return "contains invalid characters"

name = "Jack Wilde"

test = check_name(name)

if test:
    print(f"{test}")
