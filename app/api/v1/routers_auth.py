from fastapi import APIRouter, Depends, Request, Response, HTTPException
from app.core.register_user import register, login, logout
from fastapi import APIRouter, Depends, Request
from app.db.crud import create_guest_user
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas import (
    UserLogin,
    UserResponse,
    Token,
    UserBase,
    GuestUserScheme,
    UserCreate,
    VerificationCodeBase)
from app.db.crud import (
    create_guest_user,
    get_guest_by_ip,
    register_or_update_user_by_phone,
    update_verification_code,
    verify_code,
    create_verification_code,
    get_verification_code,
    delete_verification_code)
import random
from app.core.utils import send_verify_code
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
def send_verification(email: str, db: Session = Depends(get_db)):
    delete_verification_code(db, email)  # Eski kodni o'chirish
    code = send_verify_code(email)  # Yangi kod generatsiyasi va yuborish
    return create_verification_code(db, email, code)  # Kodni bazaga saqlash


# Tasdiqlash kodini tekshirish
@verify_router.post("/verification/check/")
def check_verification(data: VerificationCodeBase, db: Session = Depends(get_db)):
    verification = get_verification_code(db, data.email, data.code)

    if not verification:
        raise HTTPException(status_code=400, detail="Tasdiqlash kodi noto‘g‘ri yoki eskirgan!")

    delete_verification_code(db, data.email)  # Kodni o'chirish (bir martalik foydalanish uchun)
    return {"detail": "Tasdiqlash kodi to‘g‘ri!"}
