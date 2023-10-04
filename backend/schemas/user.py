from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(User):
    pass

class UserCreate(User):

    class Config:
        orm_mode = True