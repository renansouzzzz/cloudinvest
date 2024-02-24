from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import jwt

SECRET_KEY='planeyourlife'
ALGORITHM='HS256'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token:
    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Token inválido")
        except:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    
    def verify_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except:
            raise HTTPException( detail="Token inválido")


    @staticmethod
    def create_access_token(username: str):
        token_data = {"sub": username}
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)