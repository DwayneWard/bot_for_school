def is_email_correct(email: str) -> bool:
    if '@' in email and '.' in email:
        return True
    else:
        return False