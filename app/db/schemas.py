from datetime import datetime, timedelta
from app.enum import (ItemConditionEnum,
                      ItemImeiEnum,
                      UserGenderEnum,
                      UserRoleEnum,
                      CurrencyEnum)
from pydantic import BaseModel
from pydantic import EmailStr, Field
from typing import Optional, List

# Pydantic model - kelayotgan ma'lumotlarni tekshirib olish olish

# - - - - - - - - - CategoryBase model - - - - - - - -

class CategoryBase(BaseModel):
    category_name_uz: str
    category_name_ru: str


# - - - - - - - - - BrandBase model - - - - - - - -

class BrandBase(BaseModel):
    brand_name: str
    category_id: int


# - - - - - - - - - ModelBase model - - - - - - - -

class ModelBase(BaseModel):
    model_name: str
    brand_id: int


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
    item_barcode: str
    item_imei_status: ItemImeiEnum
    item_imei_status_2: ItemImeiEnum
    item_seria_number: Optional[str] = None

    item_purchased_price: float
    purchased_currency: CurrencyEnum
    item_purchased_quantity: int
    item_purchased_date: datetime
    previous_owner_info: str

    item_sold_price: float
    sold_currency: CurrencyEnum
    item_sold_quantity: int
    item_is_sold: Optional[bool] = False
    customer_info: str
    item_sold_date: datetime

    shop_info_id: int


# Itemni  update qilish uchun
class ItemUpdate(BaseModel):
    item_category_id: Optional[int] = None
    item_brand_id: Optional[int] = None
    item_model_id: Optional[int] = None
    item_color: Optional[str] = None
    item_ram: Optional[int] = None
    item_is_new: Optional[ItemConditionEnum] = Field(default=None)
    item_description: Optional[str] = None
    item_imei: Optional[str] = None
    item_imei_2: Optional[str] = None
    item_imei_status: Optional[ItemImeiEnum] = Field(default=None)
    item_imei_status_2: Optional[ItemImeiEnum] = Field(default=None)
    item_barcode: Optional[str] = None
    item_seria_number: Optional[str] = None
    item_purchased_price: Optional[float] = None
    purchased_currency: Optional[CurrencyEnum] = Field(default=None)
    item_purchased_quantity: Optional[int] = None
    previous_owner_info: Optional[str] = None
    item_sold_price: Optional[float] = None
    sold_currency: Optional[CurrencyEnum] = Field(default=None)
    item_sold_quantity: Optional[int] = None
    item_is_sold: Optional[bool] = None
    customer_info: Optional[str] = None
    shop_info_id: Optional[int] = None


# - - - - - - - - -  Item search - - - - - - - - -

class ItemSearch(BaseModel):
    category: Optional[int] = None
    brand: Optional[int] = None
    model: Optional[int] = None
    item_imei: Optional[str] = None
    item_imei_2: Optional[str] = None
    barcode: Optional[str] = None


# - - - - - - - - - Sell Item Schema - - - - - - - -

class SellItemSchema(BaseModel):
    sold_price: float
    sold_currency: CurrencyEnum
    sold_quantity: int
    customer_info: Optional[str] = None
    sold_date: datetime


# - - - - - - - - - UserBase model - - - - - - - -

class UserBase(BaseModel):
    user_firstname: str
    user_lastname: str
    user_email: EmailStr  # Username sifatida email kiritilishi kerak !!!
    user_phone_number: str
    user_password: str
    user_image: Optional[str] = None
    user_gender: UserGenderEnum
    is_verified: bool
    role: UserRoleEnum
    ip_address: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    user_firstname: str
    user_lastname: str
    user_email: EmailStr  # Username sifatida email kiritilishi kerak !!!
    user_phone_number: str
    user_password: str
    user_image: Optional[str] = None
    user_gender: UserGenderEnum
    is_verified: bool
    role: UserRoleEnum

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int
    user_firstname: str
    user_lastname: str
    user_email: Optional[str] = None  # Username sifatida email kiritilishi kerak !!!
    user_phone_number: Optional[str] = None
    user_image: Optional[str] = None
    user_gender: Optional[UserGenderEnum] = None
    role: UserRoleEnum
    is_verified: Optional[bool] = False
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


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


class GuestUserScheme(BaseModel):
    id: int
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    ip_address: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
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


# - - - - - - - - - VerificationCode model - - - - - - - -

class VerificationCodeBase(BaseModel):
    email: EmailStr
    code: str


class SendVerificationCode(BaseModel):
    email: EmailStr


# - - - - - - - - Hisobot yaratish - - - - - - - - - -

class ReportSchema(BaseModel):
    period: str
    total_income: float
    total_expense: float
