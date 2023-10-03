from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from fastapi_utils.guid_type import GUID

from backend.schemas import UserCreate, UserUpdate

from .config.database import get_db, Base, engine

from .models import UserTeste, User
        
app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/users")
async def get_user(db: Session = Depends(get_db)):
    return db.query(UserTeste).all() 

@app.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(payload: UserUpdate, id: GUID, db: Session = Depends(get_db)):
    updated = User(**payload.dict())
    db.query(f'UPDATE users SET name = {updated.name}, email = {updated.email}, password = {updated.password} where id = {id}')
    db.execute()
    db.commit()
    db.refresh()
    return updated