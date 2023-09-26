from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse


from .config.database import SessionLocal, engine
from sqlalchemy.orm import Session

from . import models

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
    
app = FastAPI()

@app.get("/users")
def get_user(db: Session = Depends(get_db)):
    return JSONResponse(content=db.query(models.User).all()) 

@app.post("/users/create")
def create_user(db: Session, user: models.User.email):
    hash_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hash_password=hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  