from app.core.security import create_access_token, verify_password, create_refresh_token
from app.db.crud import get_user_by_email, create_user, save_refresh_token
from app.db.schemas import UserLogin, UserBase, TokenRefreshRequest
from app.core.config import settings
from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from app.db.session import get_db
from datetime import timedelta
from app.db.models import User
from jose import JWTError
import logging
import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register(user: UserBase, db: Session = Depends(get_db)):
    db_user_email = get_user_by_email(db, user.user_email)  # Foydalanuvchi borligini tekshirish
    if db_user_email:
        raise HTTPException(status_code=409, detail="Bu email address bilan allaqachon ro'yxatdan o'tilgan!")

    return create_user(db, user)


def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.user_email)
    if not db_user or not verify_password(user.password, db_user.user_password):
        raise HTTPException(status_code=401, detail="Noto'g'ri username yoki password kiritildi!")

    logger.info("User Password:", user.password)
    logger.info("DB Password:", db_user.user_password)
    logger.info("Verify Result:", verify_password(user.password, db_user.user_password))

    # JWT token yaratish
    access_token = create_access_token(
        data={"sub": db_user.user_email},
        expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # return {"access_token": access_token, "token_type": "bearer"}

    refresh_token = create_refresh_token(
        data={"sub": db_user.user_email},
        expire_delta=timedelta(days=30)
    )

    logger.info(f"Yaratilgan refresh_token: {refresh_token}")

    # Refresh tokenni bazaga saqlash
    save_refresh_token(db, db_user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def logout():
    return {"message": "Foydalanuvchi muvaffaqiyatli o'chirildi (Frontendda token o'chirib qo'yilish kerak!)"}

