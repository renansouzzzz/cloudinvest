from pydantic import BaseModel, EmailStr, validator

from enum import Enum

from models.validators.user_validator import UserValidation


class TypeProfileEnumDTO(Enum):
    Devedor = 0
    Intermediario = 1
    Investidor = 2

class User(UserValidation):
    name: str
    email: EmailStr
    password: str
    #type_profile: TypeProfileEnumDTO

    
class UserUpdate(User):
    pass

class UserCreate(User):

    class Config:
        orm_mode = True