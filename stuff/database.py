from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./movies.db"  # Путь к файлу базы данных SQLite

# создаем к движку по url
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# настраиваем сессии для подключение к дб
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для создания моделей базы данных
Base = declarative_base()