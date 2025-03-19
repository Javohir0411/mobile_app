from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import except_
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Brand, Item, Model, ShopInfo, Category
import redis
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host="127.0.0.1",  # Redis serverining manzili (localhost yoki server IP-si)
    port=6379,  # Redis porti (standart - 6379)
    db=0,  # Redisda qaysi bazadan foydalanish (standart - 0)
    decode_responses=True  # Natijalarni string formatida qaytarish
)


# ------------ Kategoriyadan foydalanib brandning nomini olish --------------

def get_brands_by_category(category_id: int, db: Session):
    try:
        cache_key = f"brands:{category_id}"  # redis kesh kaliti
        cached_data = redis_client.get(cache_key)  # keshdan ma'lumotni sinxron tarzda olish

        if cached_data:
            logger.info(f"Cache olindi: {cached_data}")
            return json.loads(cached_data)  # keshda ma'lumot bo'lsa, o'qib qaytarish

        logger.info("Bazadan so‘rov yuborilmoqda...")  # Debug uchun

        # category_exists = db.query(Category).filter(Category.id == category_id).first()
        # if not category_exists:
        #     raise HTTPException(status_code=404, detail="Mavjud bo'lmagan category_id berildi !")

        # keshda bo'lmasa, bazadan ma'lumotni olish
        # `brand` jadvalidan to‘g‘ridan-to‘g‘ri olish
        brands = db.query(Brand).filter(Brand.category_id == category_id).all()

        logger.info(f"Topilgan brandlar: {brands}")

        # brand ro'yxatini formatlash
        brand_list = [{"id": brand.id, "name": brand.brand_name} for brand in brands]

        logger.info(f"Keshga saqlanmoqda: {brand_list}")

        # keshga 3600 soniya = 1 soatga muddatga saqlash
        redis_client.setex(cache_key, 3600, json.dumps(brand_list))
        return brand_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brandni olish uchun to'g'ri attribute kelmadi: {e}")


# ------------ Branddan foydalanib modelning nomini olish --------------

def get_models_by_brand(brand_id: int, db: Session):
    try:
        cache_key = f"models: {brand_id}"
        cached_data = redis_client.get(cache_key)

        if cached_data:
            logger.info(f"Cache olindi: {cached_data}")
            return json.loads(cached_data)

        logger.info("Bazadan so'rov yuborimoqda...")

        brand_exists = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand_exists:
            raise HTTPException(status_code=404, detail="Mavjud bo'lmagan brand_id berildi !")

        models = db.query(Model).filter(Model.brand_id == brand_id).all()
        logger.info(f"Topilgan modellar: {models}")

        # brand ro'yxatini formatlash
        model_list = [{"id": model.id, "name": model.model_name} for model in models]

        logger.info(f"Keshga saqlanmoqda: {model_list}")

        # keshga 3600 soniyaga saqlanmoqda
        redis_client.setex(cache_key, 3600, json.dumps(model_list))
        return model_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model olish uchun to'g'ri attribute kelmadi: {e}")


# ---------------- INN raqam bo'yicha tashkilotni olish -------------

def get_organization_by_inn(inn: int, db: Session):
    org = db.query(ShopInfo).filter(ShopInfo.inn_number == inn).first()
    if not org:
        logger.info("INN bo'yicha, Tashkilotni topib bo'lmadi")
        raise HTTPException(status_code=404, detail="INN bo'yicha, Tashkilotni topib bo'lmadi")

    return {"organization_name": org.company_name, "owner": org.founders}

# ------------ Item obyektini avtomatik to'ldirish ---------------

def get_latest_item(category_id: int, brand_id: int, model_id: int, db: Session = Depends(get_db)):
    latest_item = (
        db.query(Item)
        .filter(
            Item.item_category_id == category_id,
            Item.item_brand_id == brand_id,
            Item.item_model_id == model_id
        )
        .order_by(Item.created_at.desc())  # Eng oxirgi qo‘shilgan item
        .first()
    )

    return latest_item if latest_item else {}