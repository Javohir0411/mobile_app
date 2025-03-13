from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        Enum,
                        Text,
                        Float,
                        DateTime,
                        func,
                        ARRAY,
                        Boolean)
from app.enum import (ItemConditionEnum,
                      ItemImeiEnum,
                      UserGenderEnum, UserRoleEnum)
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    category_name_uz = Column(String, nullable=False)
    category_name_ru = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, primary_key=True)
    brand_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    item_category_id = Column(Integer, ForeignKey("category.id"))
    item_category = relationship("Category")
    item_brand_id = Column(Integer, ForeignKey("brand.id"))
    item_brand = relationship("Brand")
    item_model_id = Column(Integer, ForeignKey("model.id"))
    item_model = relationship("Model")
    item_color = Column(String(50), nullable=False)
    item_ram = Column(Integer)
    item_is_new = Column(Enum(ItemConditionEnum))
    item_description = Column(Text)
    item_imei = Column(String(20))
    item_imei_2 = Column(String(20))
    item_imei_status = Column(Enum(ItemImeiEnum))
    item_imei_status_2 = Column(Enum(ItemImeiEnum))
    item_seria_number = Column(String)
    item_purchased_price = Column(Float, nullable=False)
    item_selling_price = Column(Float)
    item_quantity = Column(Integer)
    shop_info_id = Column(Integer, ForeignKey("shop_info.id"))  # Do'kon egasini ma'lumotlari modeling ulanish
    shop_info = relationship("ShopInfo")  # Do'kon egasi ma'lumotlari modelidan ma'lumot olish
    customer_info = Column(Text)  # Mahsulotni do'kondan sotib olgan inson ma'lumotlari
    previous_owner_info = Column(Text)  # Mahsulotni do'konga sotib ketgan inson ma'lumotlari
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_firstname = Column(String)
    user_lastname = Column(String)
    user_email = Column(String, unique=True, index=True)  # Username sifatida email kiritilishi kerak !!!
    user_phone_number = Column(String, unique=True)  # ro'yxatdan o'tmaganlar uchun None bo'ladi
    user_password = Column(String)
    user_image = Column(String)
    user_gender = Column(Enum(UserGenderEnum), default=UserGenderEnum.OTHER)
    is_verified = Column(Boolean, default=False)  # telefon raqam tasdiqlanganmi yoki yo'q
    role = Column(Enum(UserRoleEnum),
                  default=UserRoleEnum.GUEST)  # guest - ro'yxatdan o'tmagan, user - ro'yxatdan o'tgan
    ip_address = Column(String)
    verification_code = Column(String)  # Tasdiqlash kodi
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class ShopInfo(Base):
    __tablename__ = "shop_info"

    id = Column(Integer, primary_key=True)
    register_date = Column(String, nullable=True)
    org_status = Column(String, nullable=True)
    registration_authority = Column(String, nullable=True)
    inn_number = Column(Integer)
    thsht_info = Column(String, nullable=True)
    dbibt_info = Column(String, nullable=True)
    ifut_info = Column(String, nullable=True)
    authorized_fund = Column(Float)
    org_email = Column(String, nullable=True)
    org_phone_number = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    company_address = Column(String, nullable=True)
    founders = Column(ARRAY(String))


class VerificationCode(Base):
    __tablename__ = "verification_code"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))
