from fastapi import HTTPException
from sqlalchemy.orm import Session
from config.database import engine
from schemas.user import UserSchema

def authenticate_user(email, password):
    with Session(engine) as session:
        user = session.query(UserSchema).filter(UserSchema.email == email).first()
        if not user or user.password != password:
            raise HTTPException(status_code=400, detail='Usuário não autenticado!')
        return user