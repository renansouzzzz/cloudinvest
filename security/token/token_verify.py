from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt

SECRET_KEY='planeyourlife'
ALGORITHM='HS256'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token:
    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )


    @staticmethod
    def create_access_token(username: str):
        token_data = {"sub": username}
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)