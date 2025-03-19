from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
from jose import jwt, JWTError
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 uchun token olish marshruti
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


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


def create_refresh_token(data: dict, expire_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    expire = datetime.now() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# --------- Foydalanuvchini token orqali aniqlash -----------

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             logging.info("Token noto'g'ri")
#             raise HTTPException(status_code=401, detail="Token noto'g'ri !")
#         return {"username": username}
#
#     except jwt.ExpiredSignatureError:
#         logging.info("Token muddati tugagan")
#         raise HTTPException(status_code=401, detail="Token muddati tugagan")
#
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token noto'g'ri")
