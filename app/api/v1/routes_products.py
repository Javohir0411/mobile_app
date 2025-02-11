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
from app.db.schemas import CategoryBase, BrandBase, ModelBase
from app.db.session import get_db

router = APIRouter()


# - - - - - - - - - Category - - - - - - - - -
@router.get("/categories")
def read_categories(db: Session = Depends(get_db), lang: str = "uz"):
    return get_categories(db, lang)


@router.get("/categories/{category_id}")
def read_category(category_id: int, db: Session = Depends(get_db), lang: str = "uz"):
    return get_category(db, category_id, lang)


@router.post("/categories")
def add_category(category: CategoryBase, db: Session = Depends(get_db)):
    return create_category(db, category.category_name_uz, category.category_name_ru)


@router.put("/categories/{category_id}")
def modify_category(category: CategoryBase, category_id: int, db: Session = Depends(get_db)):
    return update_category(db, category_id, category.category_name_uz, category.category_name_ru)


@router.delete("/categories/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)


# - - - - - - - - - Brands - - - - - - - - -
@router.get("/brands")
def read_brands(db: Session = Depends(get_db)):
    return get_brands(db)


@router.get("/brands/{brand_id}")
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    return get_brand(db, brand_id)


@router.post("/brands")
def add_brand(brand: BrandBase, db: Session = Depends(get_db)):
    return create_brand(db, brand.brand_name)


@router.put("/brands/{brand_id}")
def modify_brand(brand: BrandBase, brand_id: int, db: Session = Depends(get_db)):
    return update_brand(db, brand_id, brand.brand_name)

@router.delete("/brands/{brand_id")
def remove_brand(brand_id: int, db: Session = Depends(get_db)):
    return delete_brand(db, brand_id)


# - - - - - - - - - Models - - - - - - - - -
@router.get("/models")
def read_models(db: Session = Depends(get_db)):
    return get_models(db)

@router.get("/models/{model_id}")
def read_model(model_id: int, db: Session = Depends(get_db)):
    return get_model(db, model_id)

@router.post("/models")
def add_model(model: ModelBase, db: Session = Depends(get_db)):
    return create_model(db, model.model_name)

@router.put("/models/{model_id}")
def modify_model(model: ModelBase, model_id: int, db: Session = Depends(get_db)):
    return update_model(db, model_id, model.model_name)

@router.delete("/models/{model_id}")
def remove_model(model_id: int, db: Session = Depends(get_db)):
    return delete_model(db, model_id)



# - - - - - - - - - ShopInfo - - - - - - - - -