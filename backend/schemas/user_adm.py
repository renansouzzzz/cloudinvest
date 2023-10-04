from pydantic import BaseModel

class UserAdm(BaseModel):
    name: str
    email: str
    password: str
    

class UserAdmUpdate(UserAdm):
    pass

class UserAdmCreate(UserAdm):

    class Config:
        orm_mode = True