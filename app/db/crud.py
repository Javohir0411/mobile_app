from datetime import datetime, timedelta
from app.db.schemas import (UserBase,
                            UserUpdate,
                            ItemBase,
                            ItemUpdate,
                            ShopInfoBase,
                            UserRead,
                            GuestUserScheme,
                            SellItemSchema
                            )
from app.core.utils import get_translated_field
from app.db.models import User, UserRoleEnum
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from app.db.models import (Category,
                           Brand,
                           Model,
                           Item,
                           User,
                           ShopInfo,
                           VerificationCode
                           )
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Request
from app.enum import UserRoleEnum
from typing import List
from app.core.utils import send_verify_code
import logging
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ------------- Category model ------------

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


# --------------- Brand model ---------------
# Create - yangi model qo'shish
def create_brand(db: Session, brand_name: str, category_id: int):
    brand = Brand(
        brand_name=brand_name,
        category_id=category_id)
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


# ---------------- Model_name -----------------

# Create - yangi model qo'shish
def create_model(db: Session, model_name: str, brand_id: int):
    model = Model(
        model_name=model_name,
        brand_id=brand_id
    )
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


# ----------------- User model ---------------------

# Create - yangi model qo'shish
def create_user(db: Session, user: UserBase):
    hashed_password = hash_password(user.user_password)

    if not hashed_password:
        raise HTTPException(status_code=500, detail="Parolni hashlashda muammo yuz berdi")

    print(f"hashed_password: {hashed_password}")
    db_user = User(
        user_firstname=user.user_firstname,
        user_lastname=user.user_lastname,
        user_email=user.user_email,
        user_phone_number=user.user_phone_number,
        user_password=hashed_password,
        user_image=user.user_image,
        user_gender=user.user_gender
    )
    # db_user = User(**user.model_dump())
    print(f"crud.py 191 db_user: {db_user.user_email}")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Read - Barcha ma'lumotlarni o'qish
def get_users(db: Session) -> List[UserRead]:
    user_data = db.query(User).all()
    try:
        if user_data:
            logger.info(f"User modelidan olingan ma'lumotlar: {user_data} ")
            return user_data

        raise HTTPException(status_code=500, detail="User modelidan ma'lumot olib bo'lmadi!")

    except Exception as e:
        logger.info(f"User modelidan ma'lumot olishda xatolik: {e}")
        raise HTTPException(status_code=500, detail="User modelidan ma'lumot olishda xatolik yoki ma'lumot yo'q hali")


# Id bo'yicha qidirilgan userni ko'rish
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    user = db.query(User).filter(User.user_email == user_email).first()
    print("Querydan qaytgan user:", user)
    return user


def get_user_phone_number(db: Session, user_phone_number: str):
    return db.query(User).filter(User.user_phone_number == user_phone_number).first()


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


# ------------- Guest uchun crud ------------------

def create_guest_user(db: Session, ip_address: str):
    # IP manzil bo'yicha mehmon foydalanuvchi mavjudligini tekshirish
    existing_guest = db.query(User).filter_by(ip_address=ip_address, role=UserRoleEnum.GUEST.value).first()
    if existing_guest:
        logging.info(f"Mavjud mehmon topildi: {existing_guest}")
        return GuestUserScheme.model_validate(existing_guest)

    logging.info(f"Mehmon topilmadi, yaratilmoqda...")
    guest_user = User(
        user_firstname="Guest",
        user_lastname="User",
        role=UserRoleEnum.GUEST.value,
        is_verified=False,
        ip_address=ip_address
    )
    try:
        db.add(guest_user)
        db.commit()
        db.refresh(guest_user)
        logger.info(f"Guest user bazaga saqlandi: {guest_user}")
        return guest_user
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Xatolik: {e}")
        return None


# Mehmonni ip manzil orqali olish
def get_guest_by_ip(db: Session, ip_address: str):
    return db.query(User).filter(User.ip_address == ip_address, User.role == UserRoleEnum.GUEST.value).first()


# Email bilan register yoki update qilish
# def register_or_update_user_by_phone(db: Session, user_id: int, user_data: dict):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user:
#         for key, value in user_data.items():
#             setattr(user, key, value)
#         user.role = UserRoleEnum.USER.value
#         user.is_verified = True
#         db.commit()
#         db.refresh(user)
#         return user


def update_verification_code(db: Session, user_id: int, code: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.verification_code = code
        db.commit()
        db.refresh(user)
    return user


def verify_code(db: Session, email: str, code: str):
    user = db.query(User).filter(User.user_email == email, User.verification_code == code).first()
    if user:
        user.is_verified = True
        user.role = UserRoleEnum.USER.value
        user.verification_code = None  # Tasdiqlash kodini tozalash
        db.commit()
        db.refresh(user)
    return user


# --------------------------------------------------


# --------------- Item model --------------------

# Create - Yangi mahsulot qo'shish
def create_items(db: Session, items: ItemBase):
    db_item = Item(**items.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Read - Barcha ma'lumotlarni o'qish
def get_items(db: Session):
    return db.query(Item).options(
        joinedload(Item.item_category),
        joinedload(Item.item_brand),
        joinedload(Item.item_model)
    ).all()


# ID bo'yicha qidirilgan Itemni ko'rish
def get_item(db: Session, item_id: int):
    return db.query(Item).options(
        joinedload(Item.item_category),
        joinedload(Item.item_brand),
        joinedload(Item.item_model)
    ).filter(Item.id == item_id).first()


# Update - Id bo'yicha qidirilgan Itemni yangilash
def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    # Bazadagi eski obyektni olish
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_update.dict(exclude_unset=True)  # Faqat o'zgargan maydonlarni olish

    for key, value in update_data.items():
        setattr(item, key, value)  # O'zgargan maydonlarni qo'llash

    db.commit()
    db.refresh(item)
    return item


# Delete - ID bo'yicha qidirilgan Itemni o'chiramiz
def delete_item(db: Session, item_id: int):
    items = db.query(Item).filter(Item.id == item_id).first()
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(items)
    db.commit()
    return items


# ----------- Mahsulotni sotilgan deb belgilash ------------

def sell_item(item_id: int, sell_data: SellItemSchema, db: Session):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Ushbu ID bo'yicha mahsulot bazadan topilmadi !")

    print(f"Item before update: {item.item_is_sold}")

    if item.item_is_sold:
        raise HTTPException(status_code=400, detail="Bu mahsulot allaqachon sotilgan !")

    item.item_is_sold = True
    item.item_sold_price = sell_data.sold_price
    item.sold_currency = sell_data.sold_currency
    item.item_sold_quantity = sell_data.sold_quantity
    item.customer_info = sell_data.customer_info
    item.item_sold_date = sell_data.sold_date

    print(f"Item after update: {item.item_is_sold}")

    db.commit()
    db.refresh(item)
    return {"message": "Mahsulot sotildi !", "item_id": item_id}


# ----------------- ShopInfo model -------------------

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


# -------------- Verification Code ------------------

# Create - Code-ni yaratish
def create_verification_code(db: Session, email: str, code: str):
    expires_at = datetime.now() + timedelta(minutes=5)
    ver_code = VerificationCode(email=email, code=code, expires_at=expires_at)
    db.add(ver_code)
    db.commit()
    db.refresh(ver_code)
    return ver_code


# Cod-ni tekshirish
def get_verification_code(db: Session, email: str, code: str):
    result = db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.code == code
    ).first()
    return result


# Cod-ni o'chirish
def delete_verification_code(db: Session, email: str):
    db.query(VerificationCode).filter(
        VerificationCode.email == email
    ).delete()
    db.commit()


# ----------- Create Refresh Token ---------------

def save_refresh_token(db: Session, user_id: int, refresh_token: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.info(f"User topildi, token yaratilmoqda...")
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)
        logger.info(f"Refresh token bazaga yozildi: {user.refresh_token}")
        return user
    logger.info("User topilmadi !")
    return HTTPException(status_code=500, detail="User obyektini olib bo'lmadi")
