from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from app.core.config import settings


def get_db_connection():
    connection = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )
    connection.set_client_encoding('UTF8')  # Kodlashni to'g'ri qilish
    return connection


# Kirish nuqtasi
def close_db_connection(connection):
    connection.close()


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

session = SessionLocal()

