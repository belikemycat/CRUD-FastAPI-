from pydantic import BaseModel
from typing import Optional
# Базовая схема для представления данных о фильме

class UserCreate(BaseModel):
    username:str
    password:str

class User(BaseModel):
    id : int
    username : str
    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    year: int
    genre: str
    director: str
    rating: Optional[float] = None

# Схема для создания фильма (та же структура, что и у MovieBase)
class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True