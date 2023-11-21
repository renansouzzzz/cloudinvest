from fastapi import FastAPI, status

from models.user import UserCreate, UserUpdate, UserUpdateTypeProfile
from models.user_adm import UserAdmCreate, UserAdmUpdate
from models.portfolio import PortfolioCreate
from models.portfolio_datas import PortfolioDatasCreate

from config.database import Base, engine
from repository import user_repository, user_adm_repository, portfolio_repository, portfolio_datas_repository

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PlaneLife API",
    description="API > ReactNative",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(engine)

@app.get("/users", tags=['User'])
async def get_user():
        return user_repository.get()

@app.get("/users/{id}", tags=['User'])
def get_user(id: int):
        return user_repository.getById(id)

@app.post("/users/create", status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(payload: UserCreate):
        return user_repository.create(payload)

@app.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_user(user: UserUpdate, id: int):
        return user_repository.update(user, id)

@app.put("/users/update-type-profile/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_type_profile_user(id: int, typeProfile: UserUpdateTypeProfile):
        return user_repository.updateTypeProfile(id, typeProfile)

@app.delete('/users/delete/{id}', tags=['User'])
def delete_user(id: int):       
        return user_repository.delete(id)


# user adm controller --------------------------------------

@app.get("/users-adm", tags=['UserAdm'])
def get_user_adm():
        return user_adm_repository.get()

@app.post("/users-adm/create", status_code=status.HTTP_201_CREATED, tags=['UserAdm'])
def create_user_adm(payload: UserAdmCreate):
        return user_adm_repository.create(payload)

@app.put("/users-adm/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['UserAdm'])
def update_user_adm(user: UserAdmUpdate, id: int):
        return user_adm_repository.update(user, id)

@app.delete('/users-adm/delete/{id}', tags=['UserAdm'])
def delete_user_adm(id: int):       
        return user_adm_repository.delete(id)


# portfolio controller -------------
@app.get('/portfolio/{id}', status_code=status.HTTP_200_OK, tags=['Portfolio'])
def get_portfolio(id: int):
        return portfolio_repository.get(id)

@app.post('/portfolio/create', status_code=status.HTTP_201_CREATED, tags=['Portfolio'])
def create_portfolio(payload: PortfolioCreate):
        portfolio_repository.create(payload)
        
        
# portfolio datas controller ------------
@app.get('/portfolio-datas', status_code=status.HTTP_200_OK, tags=['Portfolio Datas'])
def get_portfolio_datas():
        return portfolio_datas_repository.get()

@app.post('/portfolio-datas/create', status_code=status.HTTP_201_CREATED, tags=['Portfolio Datas'])
def create_portfolio_datas(payload: PortfolioDatasCreate):
        return portfolio_datas_repository.create(payload)