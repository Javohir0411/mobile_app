import os

from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1 import routes_products, routes_sales
from app.db.session import get_db

app = FastAPI()

# Mahsulotlar API marshrutlarini ro'yxatdan o'tkazish
app.include_router(routes_products.router)

app.include_router(routes_sales.router)


def read_root():
    connection = get_db()  # Ma'lumotlar bazasiga ulanish
    # Burada boshqa ma'lumotlar olish yoki qo'shimcha ishlar qilish mumkin
    return {"message": "Connected to DB!"}
