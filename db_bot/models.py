from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import sqlalchemy as sq

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(sq.Integer, primary_key=True)
    vk_id = Column(sq.Integer, unique=True)
    first_name = Column(sq.String(100), nullable=False)
    last_name = Column(sq.String(100), nullable=False)
    age = Column(sq.Integer)
    gender = Column(sq.String(1))  # M/F
    city = Column(sq.String(50))

    def __repr__(self):
        return f"<User(vk_id={self.vk_id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

class ProfilePhoto(Base):
    __tablename__ = 'profile_photo'

    id = Column(sq.Integer, primary_key=True)
    user_id = Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    photo_url = Column(sq.String, nullable=False)

    user = relationship("User")

    def __repr__(self):
        return f"<ProfilePhoto(user_id={self.user_id}, photo_url='{self.photo_url}')>"

class FavoriteUser(Base):
    __tablename__ = 'favorite_user'

    id = Column(sq.Integer, primary_key=True)
    user_id = Column(sq.Integer, sq.ForeignKey('users.id'))
    favorited_by = Column(sq.Integer, sq.ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])
    favoriter = relationship("User", foreign_keys=[favorited_by])

    def __repr__(self):
        return f"<FavoriteUser(user_id={self.user_id}, favorited_by={self.favorited_by}, created_at={self.created_at})>"

class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(sq.Integer, primary_key=True)
    user_id = Column(sq.Integer, sq.ForeignKey('users.id'))
    blocked_by = Column(sq.Integer, sq.ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())

    blocked_user = relationship("User", foreign_keys=[user_id])
    blocker = relationship("User", foreign_keys=[blocked_by])

    def __repr__(self):
        return f"<Blacklist(blocked_user_id={self.blocked_user_id}, blocked_by={self.blocked_by}, created_at={self.created_at})>"