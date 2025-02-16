from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        Enum,
                        Text,
                        Float,
                        DateTime,
                        func, ARRAY)
from app.enum import (ItemConditionEnum,
                      ItemImeiEnum,
                      UserGenderEnum)
from sqlalchemy.orm import relationship
from .base import Base


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


class InputInnNumber(Base):
    __tablename__ = "input_inn_number"

    id = Column(Integer, primary_key=True)
    seller_inn_number = Column(String, nullable=False)
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

    id = Column(Integer, primary_key=True)
    user_firstname = Column(String, nullable=False)
    user_lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)  # Username sifatida email kiritilishi kerak !!!
    user_phone_number = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_image = Column(String)
    user_gender = Column(Enum(UserGenderEnum))
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash

class ShopInfo(Base):
    __tablename__ = "shop_info"

    id = Column(Integer, primary_key=True)
    register_date = Column(String)
    org_status = Column(String)
    registration_authority = Column(String)
    inn_number = Column(Integer)
    thsht_info = Column(String)
    dbibt_info = Column(String)
    ifut_info = Column(String)
    authorized_fund = Column(Float)
    org_email = Column(String)
    org_phone_number = Column(String)
    company_name = Column(String)
    company_address = Column(String)
    founders =  Column(ARRAY(String))
