from pydantic import BaseModel

from enum import Enum


class TypeProfileEnumDTO(Enum):
    Devedor = 0
    Intermediario = 1
    Investidor = 2

class User(BaseModel):
    name: str
    email: str
    password: str
    #type_profile: TypeProfileEnumDTO
    

class UserUpdate(User):
    pass

class UserCreate(User):

    class Config:
        orm_mode = True