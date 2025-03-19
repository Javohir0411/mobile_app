import redis
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.dynamic_search import get_brands_by_category, get_models_by_brand, get_organization_by_inn, get_latest_item

router = APIRouter()


@router.get("/brands-by-category")
def read_brands_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_brands_by_category(category_id, db)

@router.get("/models-by-brands")
def read_models_by_brand(brand_id: int, db: Session = Depends(get_db)):
    return get_models_by_brand(brand_id, db)

@router.get("/shops-by-inn")
def read_organization_by_inn(inn: int, db: Session = Depends(get_db)):
    return get_organization_by_inn(inn, db)

@router.get("/latest-item")
def read_last_item(category_id: int, brand_id: int, model_id: int, db: Session = Depends(get_db)):
    return get_latest_item(category_id, brand_id, model_id, db)