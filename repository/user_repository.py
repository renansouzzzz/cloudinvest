from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import UserCreate, UserUpdate
from ..schemas.user import UserMapped, UserSchema, UserSchema

from ..config.database import engine


def get():
    with Session(engine) as session:
        return session.query(UserMapped).all()  

def create(payload: UserCreate):
    with Session(engine) as session:
        user = UserSchema(**payload.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update(user: UserUpdate, id: int):
    with Session(engine) as session:
        getUserById = session.query(UserSchema).filter(UserSchema.id == id).one_or_none()
        if not getUserById:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        for var, value in vars(user).items():
            setattr(getUserById, var, value)
        session.add(getUserById)
        session.commit()
        session.refresh(getUserById)
        return getUserById
    
    """
    _delete apenas desativa o campo ACTIVE_
    """
def delete(id: int):
    with Session(engine) as session:
        getUser = session.get(UserSchema, id)
        if not getUser:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        session.execute(f"UPDATE user SET active = false WHERE id = {id}")
        session.commit()  
        return "Deletado com sucesso!"    