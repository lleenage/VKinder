import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

load_dotenv()  # загружает переменные окружения из файла .env

# Получаем значения из переменной окружения
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

engine = create_engine(f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    city = Column(String)

    profile_photo = relationship('ProfilePhoto', uselist=False, back_populates='user')

    # Указываем явные внешние ключи для связи через промежуточную таблицу
    favorite_user = relationship(
        'User',
        secondary='favorite_user_relation',
        primaryjoin='User.id == FavoriteUserRelation.favoriter_id',
        secondaryjoin='User.id == FavoriteUserRelation.favored_id',
        backref='favorited_by'
    )


class ProfilePhoto(Base):
    __tablename__ = 'profile_photos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    photo_url = Column(String)

    # Удалено backref='user', так как оно создается автоматически
    user = relationship('User', back_populates='profile_photo')


class Blacklist(Base):
    __tablename__ = 'blacklists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    blocked_user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)


class FavoriteUserRelation(Base):
    __tablename__ = 'favorite_user_relation'

    favoriter_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    favored_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


# Создание схемы базы данных
Base.metadata.create_all(engine)