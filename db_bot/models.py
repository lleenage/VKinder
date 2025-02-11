import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, backref

load_dotenv()  # загружает переменные окружения из файла .env

# Получаем значения из переменной окружения
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    city = Column(String)

    profile_photo = relationship('ProfilePhoto', uselist=False, backref='user')
    favorite_user = relationship('User', secondary='favorite_user_relation', backref='favorited_by')


class ProfilePhoto(Base):
    __tablename__ = 'profile_photos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    photo_url = Column(String)

    user = relationship('User', backref='profile_photo')


class Blacklist(Base):
    __tablename__ = 'blacklists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    blocked_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(String)


class FavoriteUserRelation(Base):
    __tablename__ = 'favorite_user_relation'

    favoriter_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    favored_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


# Создание схемы базы данных
Base.metadata.create_all(engine)