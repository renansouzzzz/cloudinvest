from fastapi import HTTPException

from repository import user_repository

def authenticate_user(email, password):
    user = user_repository.getByEmail(email)
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail='Usuário não autenticado!')
    return user