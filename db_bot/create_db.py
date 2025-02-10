import psycopg2
from connection_db import get_db_connection


def create_tables():
    """Создание таблиц в базе данных."""

    # Получаем соединение с базой данных
    connection = get_db_connection()

    cursor = connection.cursor()

    # SQL-запросы для создания таблиц
    sql_commands = [
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            vk_id BIGINT NOT NULL UNIQUE,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            age INT CHECK(age >= 18),
            gender CHAR(1) CHECK(gender IN ('M', 'F')),
            city VARCHAR(50)
        );
        """,

        """
        CREATE TABLE profile_photo (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            photo_url TEXT NOT NULL,
            likes_count INT DEFAULT 0
        );
        """,

        """
        CREATE TABLE favorite_user (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            favorited_by INT REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        """
        CREATE TABLE blacklist (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            blocked_by INT REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]

    # Выполняем каждый SQL-запрос последовательно
    for command in sql_commands:
        cursor.execute(command)

    connection.commit()
    cursor.close()
    connection.close()

    print("Все таблицы созданы.")


if __name__ == "__main__":
    create_tables()