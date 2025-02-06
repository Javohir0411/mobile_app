from app.db.models import Category, Brand, Model, Item, User, ShopInfo
from sqlalchemy.orm import Session


# Create - Yangi category qo'shish
def create_category(db: Session, category_name_uz: str, category_name_ru: str):
    product = Category(category_name_uz=category_name_uz, category_name_ru=category_name_ru)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# Read - Barcha mahsulotlarni olish
def get_categories(db: Session):
    return db.query(Category).all()

# ID bo'yicha qidirilgan kategoriyani
# olamiz
def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

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
def delete_category(db:Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category
