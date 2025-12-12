# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG
import sys
import os

# Для импортов в тестах
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Database:
    """Класс для работы с PostgreSQL"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Устанавливает соединение с базой данных"""
        try:
            print(f"🔄 Подключение к базе данных {DB_CONFIG['database']}...")

            # Подключаемся с явным указанием кодировки
            self.connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                client_encoding='UTF8'
            )

            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

            # Проверяем подключение
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()['version']

            print(f"✅ Подключение к базе данных установлено")
            print(f"📊 {version}")

            self._create_tables()

        except psycopg2.OperationalError as e:
            print(f"❌ Ошибка подключения к базе данных:")
            print(f"   Проверьте:")
            print(f"   1. Запущен ли PostgreSQL?")
            print(f"   2. Правильный ли пароль в .env файле?")
            print(f"   3. Существует ли база '{DB_CONFIG['database']}'?")
            print(f"   Подробности: {e}")
            raise
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")
            raise

    def disconnect(self):
        """Закрывает соединение с базой данных"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✅ Соединение с базой данных закрыто")

    def _create_tables(self):
        """Создает таблицы, если они не существуют"""
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

        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
        CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
        """

        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("✅ Таблицы созданы/проверены")
        except Exception as e:
            print(f"❌ Ошибка при создании таблиц: {e}")
            self.connection.rollback()
            raise

    def execute_query(self, query, params=None):
        """Выполняет SQL запрос и возвращает курсор"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            print(f"   Запрос: {query}")
            print(f"   Параметры: {params}")
            self.connection.rollback()
            raise

    def commit(self):
        """Фиксирует изменения"""
        self.connection.commit()

    def fetch_one(self):
        """Получает одну запись"""
        return self.cursor.fetchone()

    def fetch_all(self):
        """Получает все записи"""
        return self.cursor.fetchall()


# Создаем и подключаем базу данных
db = Database()
db.connect()