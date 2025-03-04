from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expire_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


#
# raw_password = "test123"
# hashed_password = hash_password(raw_password)
#
# print("Hashed password:", hashed_password)
# print("Verify:", verify_password(raw_password, hashed_password))