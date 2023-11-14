import re
from pydantic import BaseModel, validator

class UserValidation(BaseModel):
    
    @validator("name")
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("O nome não deve ter menos de 3 caracteres!")
        else:
            return value
        
        
    # @validator('password')
    # def valid_password(password: str):
    #     if not len(password) < 8:
    #         return True
    #     else: 
    #         raise ValueError("A senha deve ter pelo menos 8 caracteres!")