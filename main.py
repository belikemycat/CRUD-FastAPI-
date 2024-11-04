from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from stuff import database, models, schemas
from stuff.utils import get_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
app = FastAPI()
from pydantic import BaseModel
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
class UserCreate(BaseModel):
    username:str
    password:str

@app.post("/register")
async def register_user(user:UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username":new_user.username,"message":"User successfully registered!"}

@app.get("/users",response_model=list[schemas.User])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    # Создаем экземпляр фильма из данных, полученных в запросе
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)  # Добавляем фильм в сессию
    db.commit()  # Фиксируем изменения в базе данных
    db.refresh(db_movie)  # Обновляем объект db_movie после добавления
    return db_movie  # Возвращаем добавленный фильм

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    return movies


@app.get("/movies/search/", response_model=list[schemas.Movie])
def search_movie(id: int = None, title: str = None, year: int = None, genre: str = None, director:str = None, db: Session = Depends(get_db)):
    query = db.query(models.Movie)
    if director is not None:
        query = query.filter(models.Movie.director.ilike(f"%{director}%"))
    if genre is not None:
        query = query.filter(models.Movie.genre.ilike(f"%{genre}%"))
    if title is not None:
        query = query.filter(models.Movie.title.ilike(f"%{title}%"))
    if id is not None:
        query = query.filter(models.Movie.id == id)
    if year is not None:
        query = query.filter(models.Movie.year == year)
    movies = query.all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found with given parameters")

    return movies

@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    # Ищем фильм по ID
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Обновляем поля объекта фильма
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)

    db.commit()  # Сохраняем изменения
    db.refresh(db_movie)  # Обновляем объект фильма
    return db_movie  # Возвращаем обновленный фильм


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    # Ищем фильм по ID
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie NOT blyad found")

    db.delete(db_movie)
    db.commit()
    return {"detail": "Movie deleted"}
