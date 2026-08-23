from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import jwt,os

ph = PasswordHasher()
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

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

def create_access_token(user_id):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),                               # Subject (the user)
        "iat": now,            # Issued At time
        "exp": now + timedelta(minutes=60)  # Expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

    

