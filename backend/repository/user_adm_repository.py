from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.user_adm import UserAdm, UserAdmCreate, UserAdmUpdate

from ..config.database import Base, engine

from ..models.models import UserAdmMapped, UserAdmSchema
        
app = FastAPI()

Base.metadata.create_all(engine)


def get():
    with Session(engine) as session:
        return session.query(UserAdmMapped).all()  

def create(payload: UserAdmCreate):
    with Session(engine) as session:
        user = UserAdmSchema(**payload.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update(user: UserAdmUpdate, id: int):
    with Session(engine) as session:
        session_user = session.query(UserAdmSchema).filter(UserAdmSchema.id == id).one_or_none()
        if not session_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        for var, value in vars(user).items():
            setattr(session_user, var, value)
        session.add(session_user)
        session.commit()
        session.refresh(session_user)
        return session_user

def delete(id: int):
    with Session(engine) as session:
        getUser = session.get(UserAdmSchema, id)
        if not getUser:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        session.delete(getUser)
        session.commit()  
        return "Deletado com sucesso!"    