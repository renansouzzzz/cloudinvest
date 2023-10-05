from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate, UserUpdate

from ..config.database import Base, engine

from ..models.models import UserMapped, User
        
app = FastAPI()

Base.metadata.create_all(engine)

def get():
    with Session(engine) as session:
        return session.query(UserMapped).all()  

def create(payload: UserCreate):
    with Session(engine) as session:
        user = User(**payload.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update(user: UserUpdate, id: int):
    with Session(engine) as session:
        getUserById = session.query(User).filter(User.id == id).one_or_none()
        if not getUserById:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        for var, value in vars(user).items():
            setattr(getUserById, var, value)
        session.add(getUserById)
        session.commit()
        session.refresh(getUserById)
        return getUserById

def delete(id: int):
    with Session(engine) as session:
        getUser = session.get(User, id)
        if not getUser:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        session.delete(getUser)
        session.commit()  
        return "Deletado com sucesso!"    