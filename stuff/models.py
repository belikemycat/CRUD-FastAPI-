from sqlalchemy import Column,String,Integer,Float
from stuff.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=False)
    hashed_password = Column(String,nullable=False)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    year = Column(Integer,index=True)
    genre = Column(String,index=True)
    director = Column(String,index=True)
    rating = Column(Float,index=True)