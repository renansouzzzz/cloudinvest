import re
from pydantic import validator


@validator('name')
def valid_name(name: str):
    if len(name) < 3:
        raise ValueError("O nome não deve ter números!")
    
    elif re.search('\d', name):
        raise ValueError("O nome não deve ter números!")
    
    elif not len(name) < 3:
        raise ValueError("O nome não deve ter números!")
    
@validator('password')
def valid_password(password: str):
    if not len(password) < 8:
        return True
    else: 
        raise ValueError("A senha deve ter pelo menos 8 caracteres!")