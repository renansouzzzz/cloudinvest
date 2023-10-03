from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool   

class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):

    class Config:
        orm_mode = True
