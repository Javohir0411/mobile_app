from fastapi import APIRouter

router = APIRouter()


@router.get("/sales")
def get_sales():
    return {"message": {"Bu yerda barcha sotuvlar ro'yxati ko'rinadi"}}


@router.post("/sales")
def create_sale(sale_data: dict):
    # Bu yerda sotuvni bazaga qo'shish kodini yozamiz
    return {"message": "Sotuv muvaffaqiyatli qo'shildi", "sale_data": sale_data}


@router.get("/sales/{sale_id}")
def get_sale(sale_id: int):
    # Bu yerda sotuv ma'lumotlarini olish uchun kod bo'ladi
    return {"message": f"Sotuv {sale_id} ma'lumotlari"}
