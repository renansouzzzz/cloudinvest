from pydantic import BaseModel, EmailStr, Field

class UserAdm(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., regex='^(?=.*\d).{8,}$')

class UserAdmUpdate(UserAdm):
    pass

class UserAdmCreate(UserAdm):

    class Config:
        orm_mode = True