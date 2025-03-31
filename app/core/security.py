from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, Security
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
from jose import jwt, JWTError
import logging

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

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


def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get("user_id")
        is_registered: bool = payload.get("is_registered")

        if not user_id or is_registered:
            raise HTTPException(status_code=403, detail="Foydalanuvchi ro'yxatdan o'tmagan yoki no'to'gri ekan")

        user = db.query(User).filter(User.id == user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Bunday foydalanuvchi topilmadi !")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Noto'g'ri token")


def create_refresh_token(data: dict, expire_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    expire = datetime.now() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# --------- Foydalanuvchini token orqali aniqlash -----------

def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload  # Foydalanuvchi ma'lumotlarini qaytaradi
    except JWTError:
        raise HTTPException(status_code=403, detail="Token noto'g'ri yoki muddati tugagan")
