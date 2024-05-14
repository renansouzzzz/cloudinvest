from pydantic import BaseModel, EmailStr, Field

from enum import Enum


class TypeProfileEnumDTO(Enum):
    Devedor = "Devedor"
    Intermediario = "Intermediário"
    Investidor = "Investidor"


class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., regex='^(?=.*\d).{8,}$')


class UserUpdateTypeProfile(BaseModel):
    type_profile: TypeProfileEnumDTO


class UserUpdate(User):
    pass


class UserCreate(User):
    pass
