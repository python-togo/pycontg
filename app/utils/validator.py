import re


def is_valid_email(email):
    """
    Validate an email address using a regular expression.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_phone(phone):
    """
    Validate a phone number using a regular expression.
    """
    phone = phone.replace(" ", "")
    phone_regex = r'^\+?[1-9]\d{8,14}$'
    return re.match(phone_regex, phone) is not None

def is_valid_username(username):
    """
    Validate a username using a regular expression.
    """
    username_regex = r'^[a-zA-Z0-9_.-]{3,20}$'
    return re.match(username_regex, username) is not None

def is_valid_name(name):
    """
    Validate a name using a regular expression.
    """
    name_regex = r'^[a-zA-Z\s-]{1,50}$'
    return re.match(name_regex, name) is not None

def is_valid_password(password):
    """
    Validate a password using a regular expression.
    """
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None

def is_valid_url(url):
    """
    Validate a URL using a regular expression.
    """
    url_regex = r'^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/.*)?$'
    return re.match(url_regex, url) is not None