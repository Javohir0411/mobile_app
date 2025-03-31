import redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Item  # Modelni tekshiring
from app.db.dynamic_search import (
    get_brands_by_category,
    get_models_by_brand,
    get_organization_by_inn,
    get_latest_item,
    search_items
)

router = APIRouter()


# @router.get("/brands-by-category")
# def read_brands_by_category(category_id: int, db: Session = Depends(get_db)):
#     return get_brands_by_category(category_id, db)


@router.get("/brands-by-category")
def read_brands_by_category(category_name: str, db: Session = Depends(get_db)):
    return get_brands_by_category(category_name, db)


@router.get("/models-by-brands")
def read_models_by_brand(brand_name: str, db: Session = Depends(get_db)):
    return get_models_by_brand(brand_name, db)


@router.get("/shops-by-inn")
def read_organization_by_inn(inn: int, db: Session = Depends(get_db)):
    return get_organization_by_inn(inn, db)


@router.get("/latest-item")
def read_last_item(category_name: str, brand_name: str, model_name: str, db: Session = Depends(get_db)):
    return get_latest_item(category_name, brand_name, model_name, db)


# ----------- Search Item ----------------

@router.get("/search")
def searching_items(
        category: str = Query(None),
        brand: str = Query(None),
        model: str = Query(None),
        imei: str = Query(None),
        imei_2: str = Query(None),
        barcode: str = Query(None),
        lang: str = Query("uz"),
        db: Session = Depends(get_db)  # DB sessiyasini olish
):
    return search_items(category, brand, model, imei, imei_2, barcode, lang, db)
