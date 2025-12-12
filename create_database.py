# create_database.py
import psycopg2
from psycopg2 import sql


def create_database():
    """Создает базу данных taskmanager"""

    # Подключаемся к дефолтной базе postgres
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",  # Подключаемся к стандартной БД
        user="postgres",
        password="egor14022013"  # Замени на свой пароль!
    )
    conn.autocommit = True  # Важно для создания БД

    cursor = conn.cursor()

    try:
        # Проверяем, существует ли уже база
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'taskmanager'")
        exists = cursor.fetchone()

        if exists:
            print("✅ База данных 'taskmanager' уже существует")
        else:
            # Создаем базу данных
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('taskmanager')
            ))
            print("✅ База данных 'taskmanager' создана")

        # Создаем таблицы в новой базе (подключаемся к ней)
        conn2 = psycopg2.connect(
            host="localhost",
            port=5432,
            database="taskmanager",
            user="postgres",
            password="your_password_here"
        )
        cursor2 = conn2.cursor()

        # Создаем таблицу tasks
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            priority VARCHAR(10) CHECK (priority IN ('low', 'medium', 'high')),
            due_date DATE,
            status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'done')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor2.execute(create_table_query)
        conn2.commit()

        print("✅ Таблица 'tasks' создана")

        cursor2.close()
        conn2.close()

    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("🔄 Создание базы данных...")
    create_database()