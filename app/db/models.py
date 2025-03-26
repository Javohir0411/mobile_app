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
                        Boolean,
                        Numeric)
from app.enum import (ItemConditionEnum,
                      ItemImeiEnum,
                      UserGenderEnum, UserRoleEnum, CurrencyEnum)
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime, timedelta


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
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    category = relationship("Category", backref="brands", passive_deletes=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey("brand.id", ondelete="CASCADE"))
    brand = relationship("Brand", backref="models", passive_deletes=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Avtomatik kiritish vaqtini saqlash
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())  # Yangilangan vaqtini avtomatik saqlash


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    item_category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    item_category = relationship("Category", backref="items", passive_deletes=True)

    item_brand_id = Column(Integer, ForeignKey("brand.id", ondelete="CASCADE"))
    item_brand = relationship("Brand", backref="items", passive_deletes=True)

    item_model_id = Column(Integer, ForeignKey("model.id", ondelete="CASCADE"))
    item_model = relationship("Model", backref="items", passive_deletes=True)

    item_color = Column(String(50), nullable=False, default=None)
    item_ram = Column(Integer)
    item_is_new = Column(Enum(ItemConditionEnum))
    item_description = Column(Text, default=None)
    item_imei = Column(String(20), default=None)
    item_imei_2 = Column(String(20), default=None)
    item_imei_status = Column(Enum(ItemImeiEnum), default=ItemImeiEnum.UNREGISTERED.value)
    item_imei_status_2 = Column(Enum(ItemImeiEnum), default=ItemImeiEnum.UNREGISTERED.value)
    item_barcode = Column(String, unique=True, nullable=True, default=None)
    item_seria_number = Column(String, default=None)

    # Mahsulotni sotib olinganligi haqidagi ma'lumotlar
    item_purchased_price = Column(Float, nullable=False)
    purchased_currency = Column(Enum(CurrencyEnum), default=CurrencyEnum.UZS.value)
    item_purchased_quantity = Column(Integer, default=1)
    item_purchased_date = Column(DateTime(timezone=True), nullable=True)
    previous_owner_info = Column(Text, default=None)  # Mahsulotni do'konga sotib ketgan inson ma'lumotlari

    # Mahsulot sotilganligi haqidagi ma'lumotlar
    item_sold_price = Column(Float, nullable=True, default=None)
    sold_currency = Column(Enum(CurrencyEnum), default=CurrencyEnum.UZS.value)
    item_sold_quantity = Column(Integer, default=1)
    item_is_sold = Column(Boolean, default=False)
    item_sold_date = Column(DateTime(timezone=True), nullable=True, server_default=func.now(), onupdate=func.now())
    customer_info = Column(Text, default=None)  # Mahsulotni do'kondan sotib olgan inson ma'lumotlari

    shop_info_id = Column(Integer, ForeignKey("shop_info.id"))  # Do'kon egasini ma'lumotlari modeling ulanish
    shop_info = relationship("ShopInfo")  # Do'kon egasi ma'lumotlari modelidan ma'lumot olish
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
    refresh_token = Column(String, nullable=True)
    user_image = Column(String)
    user_gender = Column(Enum(UserGenderEnum), default=UserGenderEnum.OTHER)
    is_verified = Column(Boolean, default=False)  # telefon raqam tasdiqlanganmi yoki yo'q
    role = Column(Enum(UserRoleEnum),
                  default=UserRoleEnum.GUEST)  # guest - ro'yxatdan o'tmagan, user - ro'yxatdan o'tgan
    ip_address = Column(String)
    transaction = relationship("Transaction", back_populates="user")
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
    expires_at = Column(DateTime, default=lambda: datetime.now() + timedelta(minutes=5))


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    income = Column(Numeric(10, 2), default=0)
    expense = Column(Numeric(10, 2), default=0)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="transaction")
