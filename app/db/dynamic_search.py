from app.db.models import Brand, Item, Model, ShopInfo, Category
from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.utils import detect_language
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from sqlalchemy import except_
import logging
import redis
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host="127.0.0.1",  # Redis serverining manzili (localhost yoki server IP-si)
    port=6379,  # Redis porti (standart - 6379)
    db=0,  # Redisda qaysi bazadan foydalanish (standart - 0)
    decode_responses=True  # Natijalarni string formatida qaytarish
)


# ------------ Kategoriyadan foydalanib brandning nomini olish --------------

# def get_brands_by_category(category_id: int, db: Session):
#     try:
#         cache_key = f"brands:{category_id}"  # redis kesh kaliti
#         cached_data = redis_client.get(cache_key)  # keshdan ma'lumotni sinxron tarzda olish
#
#         if cached_data:
#             logger.info(f"Cache olindi: {cached_data}")
#             return json.loads(cached_data)  # keshda ma'lumot bo'lsa, o'qib qaytarish
#
#         logger.info("Bazadan so‘rov yuborilmoqda...")  # Debug uchun
#
#         # category_exists = db.query(Category).filter(Category.id == category_id).first()
#         # if not category_exists:
#         #     raise HTTPException(status_code=404, detail="Mavjud bo'lmagan category_id berildi !")
#
#         # keshda bo'lmasa, bazadan ma'lumotni olish
#         # `brand` jadvalidan to‘g‘ridan-to‘g‘ri olish
#         brands = db.query(Brand).filter(Brand.category_id == category_id).all()
#
#         logger.info(f"Topilgan brandlar: {brands}")
#
#         # brand ro'yxatini formatlash
#         brand_list = [{"id": brand.id, "name": brand.brand_name} for brand in brands]
#
#         logger.info(f"Keshga saqlanmoqda: {brand_list}")
#
#         # keshga 3600 soniya = 1 soatga muddatga saqlash
#         redis_client.setex(cache_key, 3600, json.dumps(brand_list))
#         return brand_list
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Brandni olish uchun to'g'ri attribute kelmadi: {e}")

def get_brands_by_category(category_name: str, db: Session):
    try:
        # Kategoriya nomidan tilni aniqlash
        lang = detect_language(category_name)

        # Kategoriya ID ni topish
        category_column = Category.category_name_uz if lang == "uz" else Category.category_name_ru
        category = db.query(Category).filter(category_column.ilike(f"%{category_name}%")).first()

        if not category:
            raise HTTPException(status_code=404, detail="Kategoriya topilmadi!")

        category_id = category.id  # ID ni olish

        # Redis kesh kalitini ID bo‘yicha yaratish
        cache_key = f"brands:{category_id}"  # ex: brands:12

        # Keshni tekshirish
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info(f"Cache olindi: {cache_key}")
            return json.loads(cached_data)

        logger.info("Bazadan so‘rov yuborilmoqda...")

        # Brandlarni olish
        brands = db.query(Brand).filter(Brand.category_id == category_id).all()
        brand_list = [{"id": brand.id, "brand_name": brand.brand_name, "category_name": category_column} for brand in
                      brands]

        # Keshga saqlash (1 soat)
        redis_client.setex(cache_key, 3600, json.dumps(brand_list))
        return brand_list

    except Exception as e:
        logger.error(f"Brandlarni olishda xatolik: {e}")
        raise HTTPException(status_code=500, detail=f"Brandlarni olishda xatolik: {e}")


# ------------ Branddan foydalanib modelning nomini olish --------------

def get_models_by_brand(brand_name: int, db: Session):
    brand = db.query(Brand).filter(Brand.brand_name.ilike(f"%{brand_name}%")).first()
    try:
        if not brand:
            raise HTTPException(status_code=404, detail="Brand topilmadi")

        brand_id = brand.id

        cache_key = f"models: {brand_id}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info(f"Cache olindi: {cache_key}")
            return json.loads(cached_data)

        logger.info("Bazadan so'rov yuborilmoqda...")

        models = db.query(Model).filter(Model.brand_id == brand_id).all()
        model_list = [{"id": model.id, "model_name": model.model_name, "brand_name": brand.brand_name} for model in
                      models]

        redis_client.setex(cache_key, 3600, json.dumps(model_list))
        return model_list

    except Exception as e:
        logger.info(f"Modellarni olishda xatolik: {e}")
        raise HTTPException(status_code=500, detail=f"Modellarni olishda xatolik: {e}")


# ---------------- INN raqam bo'yicha tashkilotni olish -------------

def get_organization_by_inn(inn: int, db: Session):
    org = db.query(ShopInfo).filter(ShopInfo.inn_number == inn).first()
    if not org:
        logger.info("INN bo'yicha, Tashkilotni topib bo'lmadi")
        raise HTTPException(status_code=404, detail="INN bo'yicha, Tashkilotni topib bo'lmadi")

    return {"organization_name": org.company_name, "owner": org.founders}


# ------------ Item obyektini avtomatik to'ldirish ---------------

def get_latest_item(category_name: str, brand_name: str, model_name: str, db: Session = Depends(get_db)):
    try:
        category_id = brand_id = model_id = None
        if category_name:
            lang = detect_language(category_name)
            category_column = Category.category_name_uz if lang == "uz" else Category.category_name_ru
            category = db.query(Category).filter(category_column.ilike(f"%{category_name}%")).first()

            if not category:
                raise HTTPException(status_code=404, detail="Kategoriyani topib bo'lmadi !")

            category_id = category.id

        if brand_name:
            brand = db.query(Brand).filter(Brand.brand_name.ilike(f"%{brand_name}%")).first()

            if not brand:
                raise HTTPException(status_code=404, detail="Brandni topib bo'lmadi !")

            brand_id = brand.id

        if model_name:
            model = db.query(Model).filter(Model.model_name.ilike(f"%{model_name}%")).first()

            if not model:
                raise HTTPException(status_code=404, detail="Modelni topib bo'lmadi !")

            model_id = model.id

        latest_item = (
            db.query(Item)
            .filter(
                Item.item_category_id == category_id,
                Item.item_brand_id == brand_id,
                Item.item_model_id == model_id
            ).options(
            joinedload(Item.item_category),
            joinedload(Item.item_brand),
            joinedload(Item.item_model)
            )
            .order_by(Item.created_at.desc())
            .first()
        )

        if latest_item:
            return latest_item
        else:
            return {"error": "Oxirgi qo'shilgan mahsulot topilmadi!"}

    except Exception as e:
        logger.error(f"Oxirgi itemni olishda xatolik: {e}")
        raise HTTPException(status_code=500, detail=f"Oxirgi itemni olishda xatolik: {e}")


# ---------------- Search bar yoki skaner orqali qidiruv ----------------

from sqlalchemy.orm import joinedload

def search_items(
        category: str = Query(None),
        brand: str = Query(None),
        model: str = Query(None),
        imei: str = Query(None),
        imei_2: str = Query(None),
        barcode: str = Query(None),
        lang: str = Query("uz"),
        db: Session = Depends(get_db)
):
    query = db.query(Item).options(
        joinedload(Item.item_category),
        joinedload(Item.item_brand),
        joinedload(Item.item_model)
    )

    if category:
        lang = detect_language(category)
        if lang == "uz":
            query = query.join(Item.item_category).filter(Category.category_name_uz.ilike(f"%{category}%"))
        else:
            query = query.join(Item.item_category).filter(Category.category_name_ru.ilike(f"%{category}%"))

    if brand:
        query = query.join(Item.item_brand).filter(Brand.brand_name.ilike(f"%{brand}%"))

    if model:
        query = query.join(Item.item_model).filter(Model.model_name.ilike(f"%{model}%"))

    if imei:
        query = query.filter(Item.item_imei == imei)

    if imei_2:
        query = query.filter(Item.item_imei_2 == imei_2)

    if barcode:
        query = query.filter(Item.item_barcode == barcode)

    logger.info(f"Searching Items with lang: {lang}")
    return query.all()

