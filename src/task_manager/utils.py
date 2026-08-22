from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """Hash the password using Argon2"""
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    "Verify if the entered password matches the one stored in DB"

    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False

