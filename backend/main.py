from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import config.database as db

app = FastAPI()
sqlite = db.SQLite

def __init__(self):
    sqlite.__init__(sqlite)
    sqlite.create_tables(sqlite)
    sqlite.insert(sqlite)
    self.select = sqlite.selectUsers(sqlite)

class User(BaseModel):
    name: str
    user: str
    
@app.get("/")
async def getUsers():
    select = await sqlite.selectUsers()
    
    return select


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    __init__(sqlite)
    