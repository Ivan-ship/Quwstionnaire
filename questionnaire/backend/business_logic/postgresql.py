from sqlalchemy import create_engine, text
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRESQL_CONNECT")

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("POstgreSQL подключилась успешно!")
except Exception as ex:
    print("Ошибка подключения!", ex)