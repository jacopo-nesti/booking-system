import re
from werkzeug.security import generate_password_hash, check_password_hash

# hash password
def hash_password(password):
    return generate_password_hash(password)

# verifica password
def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

# validazione password (lunghezza, maiscuola, minuscola, numero)
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    
    return True

# validazione email
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # standard regex per python per verificare formato email
    return re.fullmatch(pattern, email) is not None
