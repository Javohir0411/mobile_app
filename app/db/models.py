from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from app.enum import ItemConditionEnum, ItemImeiEnum

from .session import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    category_name_uz = Column(String, nullable=False)
    category_name_ru = Column(String, nullable=False)


class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True)
    brand_name = Column(String, nullable=False)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)


class ShopInfo(Base):
    __tablename__ = "shop_info"

    id = Column(Integer, primary_key=True)
    seller_inn_number = Column(String, nullable=False)


class Item(Base):
    __tablename__ = "item"

    item_category_id = Column(Integer, ForeignKey("category.id"))
    item_category = relationship("Category")
    item_brand_id = Column(Integer, ForeignKey("brand.id"))
    item_brand = relationship("Brand")
    item_model_id = Column(Integer, ForeignKey("model.id"))
    item_model = relationship("Model")
    item_color = Column(String(50))
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
    shop_info_id = Column(Integer, ForeignKey("shop_info.id"))  # Do'kon egasini ma'lumotlari modeliga ulanish
    shop_info = relationship("ShopInfo")  # Do'kon egasi ma'lumotlari modelidan ma'lumot olish
    customer_info = Column(Text)  # Mahsulotni do'kondan sotib olgan inson ma'lumotlari
    previous_owner_info = Column(Text)  # Mahsulotni do'konga sotib ketgan inson ma'lumotlari
