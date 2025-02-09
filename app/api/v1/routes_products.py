from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.crud import (create_category,
                         create_brand,
                         create_model,
                         create_shop,
                         create_user,
                         create_items
                         )
from app.db.crud import (get_categories,
                         get_category,
                         get_brands,
                         get_brand,
                         get_models,
                         get_model,
                         get_shops,
                         get_shop,
                         get_users,
                         get_user,
                         get_items,
                         get_item,
                         )
from app.db.crud import (update_category,
                         update_brand,
                         update_model,
                         update_shop,
                         update_item,
                         update_user,
                         )
from app.db.crud import (delete_category,
                         delete_brand,
                         delete_model,
                         delete_shop,
                         delete_item,
                         delete_user, )
from app.db.session import get_db

router = APIRouter()


# Routers For Categories
@router.get("/categories")
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.get("/categories/{category_id")
def read_category(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)


@router.post("/categories")
def add_category(db: Session = Depends(get_db)):
    return create_category(db)


@router.put("/categories/{category_id")
def modify_category(category_id: int, db: Session = Depends(get_db)):
    return update_category(db, category_id)


@router.delete("/categories/{category_id")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)


# Router for Brands
@router.get("/brands")
def read_brands(db: Session = Depends(get_db)):
    return get_brands(db)


@router.get("/brands/{brand_id")
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    return get_brand(db, brand_id)


@router.post("/brands")
def add_brand(db: Session = Depends(get_db)):
    return create_brand(db)


@router.put("/brands/{brand_id")
def modify_brand(brand_id: int, db: Session = Depends(get_db)):
    return update_brand(db, brand_id)

@router.delete("/brands/{brand_id")
