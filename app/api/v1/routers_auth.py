from fastapi import APIRouter, Depends, Request, Response, HTTPException, BackgroundTasks
from app.core.security import create_access_token, create_refresh_token
from app.db.crud import create_guest_user, get_user_by_email, save_refresh_token
from app.core.register_user import register, login, logout
from app.core.utils import send_verify_code
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.session import get_db
from datetime import timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from app.db.models import User
from app.db.schemas import (
    UserLogin,
    UserResponse,
    Token,
    UserBase,
    GuestUserScheme,
    UserCreate,
    VerificationCodeBase,
    SendVerificationCode,
    TokenRefreshRequest)
from app.db.crud import (
    create_guest_user,
    get_guest_by_ip,
    register_or_update_user_by_phone,
    update_verification_code,
    verify_code,
    create_verification_code,
    get_verification_code,
    delete_verification_code)
import logging
import random
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

router = APIRouter()
verify_router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register(user, db)


@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login(user, db)


@router.post("/logout")
def logout_user():
    return logout()


@router.post("/guest/", response_model=GuestUserScheme)
def add_guest_user_by_ip(request: Request, db: Session = Depends(get_db)):
    try:
        ip_address = request.headers.get("X-Forwarded-For", request.client.host)  # Qurilma Ip addressini olish
        logger.info(f"Guest foydalanuvchi IP manzili: {ip_address}")

        guest_user = create_guest_user(db, ip_address)  # create_guest_user funksiyasini chaqirish
        if guest_user:
            return guest_user  # create_guest_user funksiyasidan qaytgan natijani qaytarish
        raise HTTPException(status_code=500, detail="Mehmon foydalanuvchini yaratib bo'lmadi !")

    except Exception as e:
        logger.info(f"Mehmon foydalanuvchini yaratishda xatolik: {e}")
        raise HTTPException(status_code=500, detail=f"Ichki server xatoligi: {str(e)}")


@verify_router.post("/verification/send/")
def send_verification(data: SendVerificationCode, db: Session = Depends(get_db)):
    delete_verification_code(db, data.email)  # Eski kodni o'chirish
    code = send_verify_code( data.email)  # Yangi kod generatsiyasi va yuborish
    return create_verification_code(db, data.email, code)  # Kodni bazaga saqlash


# Tasdiqlash kodini tekshirish
@verify_router.post("/verification/check/")
def check_verification(data: VerificationCodeBase, db: Session = Depends(get_db)):
    verification = get_verification_code(db, data.email, data.code)
    logger.info(f"Tasdiqlash kodi: {verification}")

    if not verification:
        raise HTTPException(status_code=400, detail="Tasdiqlash kodi noto‘g‘ri yoki eskirgan!")

    # delete_verification_code(db, data.code)  # Kodni o'chirish (bir martalik foydalanish uchun)
    return {"detail": "Tasdiqlash kodi to‘g‘ri!"}


@router.post("/refresh", summary="Refresh Access Token")
def refresh_access_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email = payload.get("sub")

        if user_email is None:
            logger.info("User email mavjud emas")
            raise HTTPException(status_code=401, detail="Yaroqsiz token")

        user = db.query(User).filter(User.user_email == user_email).first()

        if not user:
            logger.info("User topilmadi")
            raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

        if user.refresh_token != request.refresh_token:
            logger.info("Berilgan refresh token mos kelmadi!")
            raise HTTPException(status_code=401, detail="Yaroqsiz refresh token")

        # Yangi access va refresh token yaratish
        new_access_token = create_access_token(data={"sub": user.user_email},
                                               expire_delta=timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES)))
        new_refresh_token = create_refresh_token(data={"sub": user.user_email})

        # Bazaga yangi refresh tokenni yozish
        save_refresh_token(db, user.id, new_refresh_token)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError as e:
        logger.info(f"JWTError: {e}")
        raise HTTPException(status_code=401, detail="Yaroqsiz token")

# ----------- Token orqali foydalanuvchin olish ------------

# @router.get("/profile")
# def profile(user: dict = Depends(get_current_user)):
#     return {"message": f"Salom, {user['username']}"}
