from typing import List

from app.core.utils import get_translated_field
from app.db.schemas import (UserBase,
                            UserUpdate,
                            ItemBase,
                            ItemUpdate,
                            ShopInfoBase, InputInnNumberBase, UserRead
                            )
from app.db.models import (Category,
                           Brand,
                           Model,
                           Item,
                           User,
                           ShopInfo
                           )
from sqlalchemy.orm import Session
from fastapi import HTTPException


# Category model
# Create - Yangi category qo'shish
def create_category(db: Session, category_name_uz: str, category_name_ru: str):
    category = Category(category_name_uz=category_name_uz, category_name_ru=category_name_ru)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# Read - Barcha mahsulotlarni olish
def get_categories(db: Session, lang: str = "uz"):
    categories = db.query(Category).all()
    result = []
    for cat in categories:
        name = get_translated_field(cat, lang, "category_name")
        result.append({"id": cat.id, "category_name": name})
    return result


# ID bo'yicha qidirilgan kategoriyani olamiz
def get_category(db: Session, category_id: int, lang: str = "uz"):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        return {
            "id": category.id,
            "category_name": get_translated_field(category, lang, "category_name")
        }


# ID bo'yicha qidirilgan kategoriyani yangilaymiz
def update_category(db: Session, category_id: int, category_name_uz: str, category_name_ru: str):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.category_name_uz = category_name_uz
        category.category_name_ru = category_name_ru
        db.commit()
        db.refresh(category)
    return category


# ID bo'yicha qidirilgan kategoriyani o'chiramiz
def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category


# Brand model
# Create - yangi model qo'shish
def create_brand(db: Session, brand_name: str):
    brand = Brand(brand_name=brand_name)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


# Read - Barcha ma'lumotlarni o'qish.
def get_brands(db: Session):
    return db.query(Brand).all()


# ID bo'yicha qidirilgan brand nomlarini ko'rish
def get_brand(db: Session, brand_id: int):
    return db.query(Brand).filter(Brand.id == brand_id).first()


# ID bo'yicha qidirilgan ma'lumotlarni yangilaymiz
def update_brand(db: Session, brand_id: int, brand_name: str):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand:
        brand.brand_name = brand_name
        db.commit()
        db.refresh(brand)
    return brand


# ID bo'yicha qidirilgan brandni o'chiramiz
def delete_brand(db: Session, brand_id: int):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand:
        db.delete(brand)
        db.commit()
    return brand


# Model_name uchun  model
# Create - yangi model qo'shish
def create_model(db: Session, model_name: str):
    model = Model(model_name=model_name)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


# Read - Barcha ma'lumotlarni o'qish
def get_models(db: Session):
    return db.query(Model).all()


# ID bo'yicha qidirilgan modelni ko'rish
def get_model(db: Session, model_id: int):
    return db.query(Model).filter(Model.id == model_id).first()


# ID bo'yicha qidirilgan modelni yangilash
def update_model(db: Session, model_id: int, model_name: str):
    model = db.query(Model).filter(Model.id == model_id).first()
    if model:
        model.model_name = model_name
        db.commit()
        db.refresh(model)
    return model


# ID bo'yicha qidirilgan modelni o'chiramiz
def delete_model(db: Session, model_id: int):
    model = db.query(Model).filter(Model.id == model_id).first()
    if model:
        db.delete(model)
        db.commit()
    return model


# User model
# Create - yangi model qo'shish
def create_user(db: Session, user: UserBase, ):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Read - Barcha ma'lumotlarni o'qish
def get_users(db: Session) -> List[UserRead]:
    return db.query(User).all()


# Id bo'yicha qidirilgan userni ko'rish
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.user_email == user_email).first()


def get_user_phone_number(db: Session, user_phone_number: str):
    return db.query(User).filter(User.user_phone_number == user_phone_number)


# ID bo'yicha qidirilgan userni yangilash
def update_user(user_id: int, user: UserUpdate, db: Session):
    user_items = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Faqat kiritilgan maydonni yangilash
    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user_items, key, value)

    db.commit()
    db.refresh(user_items)
    return user_items


# Delete user
# ID bo'yicha qidirilgan userni o'chiramiz
def delete_user(user_id: int, db: Session):
    user_items = db.query(User).filter(User.id == user_id).first()
    if not user_items:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_items)
    db.commit()
    return user_items


# Item model
# Create - Yangi mahsulot qo'shish
def create_items(db: Session, items: ItemBase):
    db_item = Item(**items.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Read - Barcha ma'lumotlarni o'qish
def get_items(db: Session):
    return db.query(Item).all()


# ID bo'yicha qidirilgan Itemni ko'rish
def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


# Update - Id bo'yicha qidirilgan Itemni yangilash
def update_item(db: Session, item_id: int, item: ItemUpdate):
    items = db.query(Item).filter(Item.id == item_id).first()
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(items, key, value)

    db.commit()
    db.refresh(items)
    return items


# Delete - ID bo'yicha qidirilgan Itemni o'chiramiz
def delete_item(db: Session, item_id: int):
    items = db.query(Item).filter(Item.id == item_id).first()
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(items)
    db.commit()
    return items


# ShopInfo model
# Create - Yangi do'kon qo'shish
def create_shop(db: Session, shop_data: ShopInfoBase):
    shop = ShopInfo(**shop_data.model_dump(exclude_unset=True))
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop


# Read- Barcha shopni ko'rish
def get_shops(db: Session):
    return db.query(ShopInfo).all()


# ID bo'yicha qidirilgan shopni ko'rish
def get_shop(db: Session, shop_id):
    return db.query(ShopInfo).filter(ShopInfo.id == shop_id).first()


# Update - ID bo'yicha qidirilgan shopni yangilash
def update_shop(db: Session, shop_id: int, shop_data: ShopInfoBase):
    shop = db.query(ShopInfo).filter(ShopInfo.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    for key, value in shop_data.model_dump(exclude_unset=True).items():
        setattr(shop, key, value)

    db.commit()
    db.refresh(shop)
    return shop


# Delete - ID bo'yicha qidirilgan shopni o'chiramiz
def delete_shop(db: Session, shop_id: int):
    shop = db.query(ShopInfo).filter(ShopInfo.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    db.delete(shop)
    db.commit()
    return shop
