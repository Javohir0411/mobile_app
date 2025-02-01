from fastapi import FastAPI
from app.api.v1 import routes_products, routes_sales

app = FastAPI()

# Mahsulotlar API marshrutlarini ro'yxatdan o'tkazish
app.include_router(routes_products.router)

app.include_router(routes_sales.router)
