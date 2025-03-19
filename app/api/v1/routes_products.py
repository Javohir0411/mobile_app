from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.crud import (create_category,
                         create_brand,
                         create_model,
                         create_shop,
                         create_user,
                         create_items,
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
                         delete_user,
                         )
from app.db.schemas import CategoryBase, BrandBase, ModelBase, ShopInfoBase, ItemBase, InputInnNumberBase, UserBase, \
    UserUpdate, UserRead
from app.db.session import get_db
from app.core.utils import get_shop_info

category_router = APIRouter()
brand_router = APIRouter()
model_router = APIRouter()
shop_router = APIRouter()
item_router = APIRouter()
user_router = APIRouter()


# - - - - - - - - - Category - - - - - - - - -
@category_router.get("/categories")
def read_categories(db: Session = Depends(get_db), lang: str = "uz"):
    return get_categories(db, lang)


@category_router.get("/categories/{category_id}")
def read_category(category_id: int, db: Session = Depends(get_db), lang: str = "uz"):
    return get_category(db, category_id, lang)


@category_router.post("/categories")
def add_category(category: CategoryBase, db: Session = Depends(get_db)):
    return create_category(db, category.category_name_uz, category.category_name_ru)


@category_router.put("/categories/{category_id}")
def modify_category(category: CategoryBase, category_id: int, db: Session = Depends(get_db)):
    return update_category(db, category_id, category.category_name_uz, category.category_name_ru)


@category_router.delete("/categories/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)


# - - - - - - - - - Brands - - - - - - - - -
@brand_router.get("/brands")
def read_brands(db: Session = Depends(get_db)):
    return get_brands(db)


@brand_router.get("/brands/{brand_id}")
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    return get_brand(db, brand_id)


# --------- Category-dan foydalanib brandni olish --------

# @brand_router.get("/brands-by-category")
# def read_brands_by_category(category_id: int, db: Session = Depends(get_db)):
#     return get_brands_by_category(category_id, db)


@brand_router.post("/brands")
def add_brand(brand: BrandBase, db: Session = Depends(get_db)):
    return create_brand(db, brand.brand_name, brand.category_id)


@brand_router.put("/brands/{brand_id}")
def modify_brand(brand: BrandBase, brand_id: int, db: Session = Depends(get_db)):
    return update_brand(db, brand_id, brand.brand_name)


@brand_router.delete("/brands/{brand_id}")
def remove_brand(brand_id: int, db: Session = Depends(get_db)):
    return delete_brand(db, brand_id)


# - - - - - - - - - Models - - - - - - - - -
@model_router.get("/models")
def read_models(db: Session = Depends(get_db)):
    return get_models(db)


@model_router.get("/models/{model_id}")
def read_model(model_id: int, db: Session = Depends(get_db)):
    return get_model(db, model_id)

# # --------- Brand-dan foydalanib modelni olish --------
#
# @model_router.get("/models-by-brands")
# def read_models_by_brand(brand_id: int, db: Session = Depends(get_db)):
#     return get_models_by_brand(brand_id, db)


@model_router.post("/models")
def add_model(model: ModelBase, db: Session = Depends(get_db)):
    return create_model(db, model.model_name, model.brand_id)


@model_router.put("/models/{model_id}")
def modify_model(model: ModelBase, model_id: int, db: Session = Depends(get_db)):
    return update_model(db, model_id, model.model_name)


@model_router.delete("/models/{model_id}")
def remove_model(model_id: int, db: Session = Depends(get_db)):
    return delete_model(db, model_id)


# - - - - - - - - - ShopInfo - - - - - - - - -

@shop_router.get("/shops")
def read_shops(db: Session = Depends(get_db)):
    return get_shops(db)


@shop_router.get("/shops/{shop_id}")
def read_shop(shop_id: int, db: Session = Depends(get_db)):
    return get_shop(db, shop_id)


@shop_router.post("/shops")
def add_shop_by_inn(inn_data: InputInnNumberBase, db: Session = Depends(get_db)):
    print(f"INN raqami: {inn_data.org_inn_number}")

    shop_info = get_shop_info(inn_data.org_inn_number)
    print(f"Olingan ma'lumotlar: {shop_info}")

    created_shop = create_shop(db, shop_info)
    return {"detail": "Tashkilot saqlandi", "data": created_shop}


@shop_router.put("/shop/{shop_id}")
def modify_shop(shop_id: int, shop: ShopInfoBase, db: Session = Depends(get_db)):
    return update_shop(db, shop_id, shop)


@shop_router.delete("/shops/{shop_id}")
def remove_shop(shop_id: int, db: Session = Depends(get_db)):
    return delete_shop(db, shop_id)


# - - - - - - - - - Items - - - - - - - - -

@item_router.get("/items")
def read_items(db: Session = Depends(get_db)):
    return get_items(db)


@item_router.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    return get_item(db, item_id)


@item_router.post("/items")
def add_item(item: ItemBase, db: Session = Depends(get_db)):
    return create_items(db, item)


@item_router.put("/items/{item_id}")
def modify_item(item_id: int, item: ItemBase, db: Session = Depends(get_db)):
    return update_item(db, item_id, item)


@item_router.delete("/item/{item_id}")
def remove_item(item_id, db: Session = Depends(get_db)):
    return delete_item(db, item_id)


# - - - - - - - - - User - - - - - - - -

@user_router.get("/users")
def read_users(db: Session = Depends(get_db)) -> List[UserRead]:
    return get_users(db)


@user_router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


@user_router.post("/users")
def add_user(user: UserBase, db: Session = Depends(get_db)):
    return create_user(db, user)


@user_router.put("/users/{user_id}")
def modify_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, user, db)


@user_router.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
