from app.enum import (ItemConditionEnum,
                      ItemImeiEnum,
                      UserGenderEnum
                      )
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional, List


# Pydantic model - kelayotgan ma'lumotlarni tekshirib olish olish

# - - - - - - - - - CategoryBase model - - - - - - - -

class CategoryBase(BaseModel):
    category_name_uz: str
    category_name_ru: str


# - - - - - - - - - BrandBase model - - - - - - - -

class BrandBase(BaseModel):
    brand_name: str


# - - - - - - - - - ModelBase model - - - - - - - -

class ModelBase(BaseModel):
    model_name: str


# - - - - - - - - - InputInnNumberBase model - - - - - - - -

class InputInnNumberBase(BaseModel):
    org_inn_number: int


# - - - - - - - - - ItemBase model - - - - - - - -

class ItemBase(BaseModel):
    item_category_id: int
    item_brand_id: int
    item_model_id: int
    item_color: str
    item_ram: Optional[int] = None
    item_is_new: ItemConditionEnum
    item_description: Optional[str] = None
    item_imei: Optional[str] = None
    item_imei_2: Optional[str] = None
    item_imei_status: ItemImeiEnum
    item_imei_status_2: ItemImeiEnum
    item_seria_number: Optional[str] = None
    item_purchased_price: float
    item_selling_price: float
    item_quantity: int
    shop_info_id: int
    customer_info: str
    previous_owner_info: str


# Itemni  update qilish uchun
class ItemUpdate(BaseModel):
    item_category_id: Optional[int] = None
    item_brand_id: Optional[int] = None
    item_model_id: Optional[int] = None
    item_color: Optional[str] = None
    item_ram: Optional[int] = None
    item_is_new: Optional[ItemConditionEnum]
    item_description: Optional[str] = None
    item_imei: Optional[str] = None
    item_imei_2: Optional[str] = None
    item_imei_status: Optional[ItemImeiEnum]
    item_imei_status_2: Optional[ItemImeiEnum]
    item_seria_number: Optional[str] = None
    item_purchased_price: Optional[float] = None
    item_quantity: Optional[int] = None
    shop_info_id: Optional[int] = None
    customer_info: Optional[str] = None
    previous_owner_info: Optional[str] = None


# - - - - - - - - - UserBase model - - - - - - - -

class UserBase(BaseModel):
    user_firstname: str
    user_lastname: str
    user_email: EmailStr  # Username sifatida email kiritilishi kerak !!!
    user_phone_number: str
    user_password: str
    user_image: Optional[str] = None
    user_gender: UserGenderEnum

class UserRead(BaseModel):
    id: int
    user_firstname: str
    user_lastname: str
    user_email: str  # Username sifatida email kiritilishi kerak !!!
    user_phone_number: str
    user_image: Optional[str] = None
    user_gender: UserGenderEnum

# Foydalanuvchi ma'lumotlarini qaytarish uchun model
class UserResponse(BaseModel):
    id: int
    user_email: EmailStr

    class Config:
        from_attributes = True


# Userni update qilish uchun
class UserUpdate(BaseModel):
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    user_email: Optional[EmailStr] = None  # Username sifatida email kiritilishi kerak !!!
    user_phone_number: Optional[str] = None
    user_password: Optional[str] = None
    user_image: Optional[str] = None
    user_gender: Optional[UserGenderEnum] = None


class UserLogin(BaseModel):
    user_email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# - - - - - - - - - ShopInfoBase model - - - - - - - -

class ShopInfoBase(BaseModel):
    register_date: Optional[str] = None
    org_status: Optional[str] = None
    registration_authority: Optional[str] = None
    inn_number: Optional[int] = None
    thsht_info: Optional[str] = None
    dbibt_info: Optional[str] = None
    ifut_info: Optional[str] = None
    authorized_fund: Optional[float] = None
    org_email: Optional[str] = None
    org_phone_number: Optional[str] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    founders: Optional[List[str]] = None
