from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_utils.guid_type import GUID

from backend.schemas.schemas import UserCreate, UserUpdate

from .config.database import get_db, Base, engine
from .repository import user_repository

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/users")
def get_user():
        return user_repository.get()

@app.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
        return user_repository.create(payload)

@app.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(user: UserUpdate, id: int):
        return user_repository.update(user, id)

@app.delete('/users/delete/{id}')
def delete_user(id: int):       
        return user_repository.delete(id)