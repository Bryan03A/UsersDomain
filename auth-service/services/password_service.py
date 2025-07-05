import hashlib

def hash_password(password: str) -> str:
    salt = 'salt'
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 1000, 64).hex()