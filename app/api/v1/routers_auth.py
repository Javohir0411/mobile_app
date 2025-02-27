from app.db.schemas import UserLogin, UserResponse, Token, UserBase
from app.core.register_user import register, login, logout
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserBase, db: Session = Depends(get_db)):
    return register(user, db)

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login(user, db)

@router.post("/logout")
def logout_user():
    return logout()