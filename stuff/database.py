from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./movies.db"  

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# session to connect to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for creating the database
Base = declarative_base()
