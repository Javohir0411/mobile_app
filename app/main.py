from fastapi import FastAPI, Request
from app.api.v1.routes_products import (
    category_router,
    brand_router,
    model_router,
    item_router,
    shop_router,
    user_router
)
from app.api.v1.routers_auth import router as auth_router
from app.api.v1.routers_auth import verify_router
from app.api.v1.routes_dynamic_search import router as dynamic_search
from app.api.v1.routes_sales import router as selling_info
from app.api.v1.routes_reports import report_router as income_expense
from app.api.v1.routes_exports import export_router
import uvicorn

app = FastAPI(title="My Project API", version="1.0")

routers = [
    (category_router, "Category"),
    (brand_router, "Brand"),
    (model_router, "Model"),
    (shop_router, "Shop"),
    (item_router, "Item"),
    (user_router, "User"),
    (auth_router, "Registration"),
    (verify_router, "Verification Code"),
    (dynamic_search, "Dynamic Search"),
    (selling_info, "Selling Information"),
    (income_expense, "Income and Expense"),
    (export_router, "Save to Excel and PDF")
]

for router, tag in routers:
    app.include_router(router, prefix="/api/v1", tags=[tag])


# app = FastAPI()

@app.get("/")
def get_ip(request: Request):
    user_ip = request.client.host
    return {"Sizning IP manzilingiz": user_ip}


# @app.get("/")
# def read_root():
#     return {"message": "Swagger dokumentatsiya: http://127.0.0.1:8000/docs"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
