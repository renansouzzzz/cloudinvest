from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import config.database as db
import json

app = FastAPI()
sqlite = db.SQLite

def __init__(self):
    sqlite.__init__(sqlite)
    sqlite.create_tables(sqlite)
    sqlite.insert(sqlite)

class Usuario(BaseModel):
    name: str
    user: str
    
@app.get("/select")
async def read_root():
    select = await sqlite.selectUsers(sqlite)
    list = []
    
    for user in select:
        list.append(user)
        
    return  list


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    __init__(sqlite)