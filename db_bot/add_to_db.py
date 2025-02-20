from models import engine, Base, User, ProfilePhoto, Blacklist, FavoriteUserRelation
from sqlalchemy.orm import sessionmaker

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создание схемы таблиц
Base.metadata.create_all(engine)

# Функция для добавления нового пользователя
def add_user(first_name, last_name, age=None, gender=None, city=None):
    new_user = User(first_name=first_name, last_name=last_name, age=age, gender=gender, city=city)
    session.add(new_user)
    session.commit()
    print("Пользователь добавлен:", new_user)
    return new_user

# Функция для добавления фотографии профиля
def add_profile_photo(user_id, photo_url):
    new_photo = ProfilePhoto(user_id=user_id, photo_url=photo_url)
    session.add(new_photo)
    session.commit()
    print("Фотография профиля добавлена:", new_photo)
    return new_photo

# Функция для добавления любимого пользователя
def add_favorite_user(favoriter_id, favored_id):
    relation = FavoriteUserRelation(favoriter_id=favoriter_id, favored_id=favored_id)
    session.add(relation)
    session.commit()
    print("Любимый пользователь добавлен:", relation)

# Функция для добавления пользователя в черный список
def add_to_blacklist(user_id, blocked_user_id):
    blacklist_entry = Blacklist(user_id=user_id, blocked_user_id=blocked_user_id)
    session.add(blacklist_entry)
    session.commit()
    print("Пользователь добавлен в черный список:", blacklist_entry)

# Функция для поиска пользователя по ID
def get_user_by_id(user_id):
    return (session.query(User).filter(User.id) == user_id).one_or_none()

# Функция для удаления пользователя из черного списка
def remove_from_blacklist(user_id, blocked_user_id):
    deleted = session.query(Blacklist).filter()(Blacklist.user_id) == user_id, Blacklist.blocked_user_id == blocked_user_id.delete()
    session.commit()
    if deleted > 0:
        print(f"Пользователь удалён из чёрного списка.")
    else:
        print(f"Пользователь не найден в чёрном списке.")

# Функция для удаления любимого пользователя
def remove_favorite_user(favoriter_id, favored_id):
    deleted = session.query(FavoriteUserRelation).filter()(FavoriteUserRelation.favoriter_id) == favoriter_id, FavoriteUserRelation.favored_id == favored_id.delete()
    session.commit()
    if deleted > 0:
        print(f"Отношения 'любимого пользователя' удалены.")
    else:
        print(f"Отношения 'любимого пользователя' не найдены.")