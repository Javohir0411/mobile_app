from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str  # Ma'lumot string shaklida kelishini tekshiradi

    class Config:
        env_file = ".env"  # .env faylini iavtomatik qo'shish


settings = Settings()  # settings o'zgaruvchisiga yuklash

"""
.env faylidagi manzilni pydantic tekshiradi ma'lumot bormi yoki yo'q.
Agar mavjud bo'lsa, bazaga ulanish ishlaydi, aks xolda, xatolik chiqaradi.
"""
