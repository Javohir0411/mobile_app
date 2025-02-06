from pydantic_settings import BaseSettings

#
# class Settings(BaseSettings):
#     DATABASE_URL: str  # Ma'lumot string shaklida kelishini tekshiradi
#
#     class Config:
#         env_file = ".env"  # .env faylini iavtomatik qo'shish
#
#
# settings = Settings()  # settings o'zgaruvchisiga yuklash

"""
.env faylidagi manzilni pydantic tekshiradi ma'lumot bormi yoki yo'q.
Agar mavjud bo'lsa, bazaga ulanish ishlaydi, aks xolda, xatolik chiqaradi.
"""

class Settings(BaseSettings):
    DATABASE_URL: str
    DB_NAME: str = "product_inventory"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "your_password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
