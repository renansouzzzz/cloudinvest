from msilib import schema
from fastapi import FastAPI

from .config.database import SessionLocal, engine
from sqlalchemy.orm import Session

from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users")
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

@app.post("/users/create")
def create_user(db: Session, user: schema.UserCreate):
    hash_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hash_password=hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  