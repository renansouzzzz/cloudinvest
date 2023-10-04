from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.schemas import UserCreate, UserUpdate

from ..config.database import Base, engine

from ..models.models import UserTeste, User
        
app = FastAPI()

Base.metadata.create_all(engine)


def get():
    with Session(engine) as session:
        return session.query(UserTeste).all()  

def create(payload: UserCreate):
    with Session(engine) as session:
        user = User(**payload.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update(user: UserUpdate, id: int):
    with Session(engine) as session:
        session_user = session.query(User).filter(User.id == id).one_or_none()
        for var, value in vars(user).items():
            setattr(session_user, var, value)
        session.add(session_user)
        session.commit()
        session.refresh(session_user)
        return session_user

def delete(id: int):
    with Session(engine) as session:
        getUser = session.get(User, id)
        if not getUser:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        session.delete(getUser)
        session.commit()  
        return "Deletado com sucesso!"    