from pydantic import BaseModel, EmailStr, Field

from enum import Enum


class TypeProfileEnumDTO(Enum):
    Devedor = 0
    Intermediario = 1
    Investidor = 2    
        
class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., regex='^(?=.*\d).{8,}$')

class UserUpdate(User):
    pass

class UserCreate(User):

    class Config:
        orm_mode = True