from pydantic import BaseModel
from typing import Optional
#data validatioon 
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
# to create movies, inherit from moviebase
class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True
