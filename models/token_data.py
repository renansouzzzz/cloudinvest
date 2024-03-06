from pydantic import BaseModel
from models.user import User


class TokenData(BaseModel):
    access_token: str
    user: dict