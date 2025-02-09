# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# import psycopg2
# from psycopg2 import sql
# from psycopg2.extras import RealDictCursor
# from app.core.config import settings
#
#
# def get_db_connection():
#     connection = psycopg2.connect(
#         dbname=settings.DB_NAME,
#         user=settings.DB_USER,
#         password=settings.DB_PASSWORD,
#         host=settings.DB_HOST,
#         port=settings.DB_PORT
#     )
#     connection.set_client_encoding('UTF8')  # Kodlashni to'g'ri qilish
#     return connection
#
# def get_db():
#     db = SessionLocal()  # Yangi sessiya ochamiz
#     try:
#         yield db
#     finally:
#         db.close()
#
# # Kirish nuqtasi
# def close_db_connection(connection):
#     connection.close()
#
#
# DATABASE_URL = settings.DATABASE_URL
#
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
#
# session = SessionLocal()
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# PostgreSQL bazasi bilan bog‘lanish uchun SQLAlchemy engine yaratamiz
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

# SessionLocal - Har bir so‘rov uchun yangi sessiya yaratish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def get_db():  # Har bir so‘rov uchun alohida sessiya yaratish va yopish
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # So‘rov tugagach sessiya yopiladi
