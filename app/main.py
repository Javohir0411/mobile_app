from fastapi import FastAPI
from app.api.v1.routes_products import router as product_router
import uvicorn

app = FastAPI(title="My Project API", version="1.0")

# Barcha mahsulot marshrutlarini bitta router orqali ulash
app.include_router(product_router, prefix="/api/v1",
                   tags=["Endpoints"])


@app.get("/")
def read_root():
    return {"message": "Swagger dokumentatsiya: http://127.0.0.1:8000/docs"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
