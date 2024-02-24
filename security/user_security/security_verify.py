from fastapi import HTTPException
from models.user import UserLogin

def authenticate_user(db, userPayload: UserLogin):
    user = db.get(userPayload)
    if not user or user.password != user["password"]:
        raise HTTPException(status_code=400, detail='Usuário não autenticado!')
    return user