import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем параметры подключения из переменных окружения
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

Base = declarative_base()


def get_db_session():
    # Формируем строку подключения к базе данных
    connection_string = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session()


session = get_db_session()