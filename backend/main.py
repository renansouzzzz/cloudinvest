from fastapi import FastAPI, status

from backend.schemas.user import UserCreate, UserUpdate
from backend.schemas.user_adm import UserAdmCreate, UserAdmUpdate

from .config.database import Base, engine
from .repository import user_repository, user_adm_repository, portfolio_repository as repository

app = FastAPI(
    title="PlaneLife API",
    description="API > ReactNative",
    openapi_url="/api/v1/"
)

Base.metadata.create_all(engine)

@app.get("/users", tags=['User'])
def get_user():
        return repository.get()

@app.post("/users/create", status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(payload: UserCreate):
        return repository.create(payload)

@app.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_user(user: UserUpdate, id: int):
        return repository.update(user, id)

@app.delete('/users/delete/{id}', tags=['User'])
def delete_user(id: int):       
        return repository.delete(id)


# user adm controller --------------------------------------

@app.get("/users-adm", tags=['UserAdm'])
def get_user_adm():
        return repository.get()

@app.post("/users-adm/create", status_code=status.HTTP_201_CREATED, tags=['UserAdm'])
def create_user_adm(payload: UserAdmCreate):
        return repository.create(payload)

@app.put("/users-adm/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['UserAdm'])
def update_user_adm(user: UserAdmUpdate, id: int):
        return repository.update(user, id)

@app.delete('/users-adm/delete/{id}', tags=['UserAdm'])
def delete_user_adm(id: int):       
        return repository.delete(id)


# portfolio controller -------------
@app.get('/portfolio/{id}', status_code=status.HTTP_200_OK, tags=['Portfolio'])
def get_portfolio(id: int):
        return repository.get(id)