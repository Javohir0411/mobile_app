from fastapi import APIRouter

router = APIRouter()

@router.get("/products/")
def get_products():
    return {"message": {"Bu yerda mahsulotlar ro'yxati bo'ladi"}}