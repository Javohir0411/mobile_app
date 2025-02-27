from fastapi import FastAPI
from app.api.v1.routes_products import (
    category_router,
    brand_router,
    model_router,
    item_router,
    shop_router,
    user_router,
)
from app.api.v1.routers_auth import router as auth_router
import uvicorn

app = FastAPI(title="My Project API", version="1.0")

routers = [
    (category_router, "Category"),
    (brand_router, "Brand"),
    (model_router, "Model"),
    (item_router, "Item"),
    (shop_router, "Shop"),
    (user_router, "User"),
    (auth_router, "Registration")
]

for router, tag in routers:
    app.include_router(router, prefix="/api/v1", tags=[tag])


@app.get("/")
def read_root():
    return {"message": "Swagger dokumentatsiya: http://127.0.0.1:8000/docs"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
