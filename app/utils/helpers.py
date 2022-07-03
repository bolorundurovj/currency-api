import re


def is_valid_email(email):
    """Checks if email is valid

    Args:
        email (str): Email

    Returns:
        bool: boolean
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return True if re.fullmatch(regex, email) else False
