import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URL)
database = client[DATABASE_NAME]

try:
    client.admin.command("ping")
    print("MongoDB подключилась успешно")
except Exception as e:
    print("Ошибка подключения к MongoDb:", e)