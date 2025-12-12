
import os
from dotenv import load_dotenv
import sys

# Явно указываем путь и кодировку для .env
env_path = os.path.join(os.path.dirname(__file__), '.env')

# Проверяем существование файла
if not os.path.exists(env_path):
    print(f"⚠️ Файл .env не найден по пути: {env_path}")
    print("Создайте файл .env со следующими переменными:")
    print("DB_HOST=localhost")
    print("DB_PORT=5432")
    print("DB_NAME=taskmanager")
    print("DB_USER=postgres")
    print("DB_PASSWORD=ваш_пароль")
    sys.exit(1)

# Загружаем с явным указанием кодировки
try:
    # Способ 1: Через dotenv с указанием кодировки
    load_dotenv(dotenv_path=env_path, encoding='utf-8')

    # Проверяем, что переменные загрузились
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ В .env файле отсутствуют переменные: {', '.join(missing_vars)}")
        sys.exit(1)

except Exception as e:
    print(f"❌ Ошибка при загрузке .env файла: {e}")
    print("Проверьте кодировку файла .env (должна быть UTF-8 без BOM)")
    sys.exit(1)

# Конфигурация базы данных
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "client_encoding": "utf8",  # Явно указываем кодировку для соединения
}

# Вывод для отладки (можно убрать после настройки)
print(f"✅ Конфигурация БД загружена:")
print(f"   Хост: {DB_CONFIG['host']}")
print(f"   База: {DB_CONFIG['database']}")
print(f"   Пользователь: {DB_CONFIG['user']}")