from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

from models.user import UserCreate, UserUpdate, UserUpdateTypeProfile
from models.user_adm import UserAdmCreate, UserAdmUpdate
from models.portfolio import PortfolioCreate
from models.portfolio_datas import PortfolioDatasCreate

from config.database import Base, engine
from repository import user_repository, user_adm_repository, portfolio_repository, portfolio_datas_repository

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.openapi.utils import get_openapi
from security.token.token_verify import Token

from security.user_security.security_verify import authenticate_user

origins = [
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.get("/")
async def read_root():
    return {"message": "API EXECUTADA COM SUCESSO!"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário ou senha inválidos',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return Token.create_access_token(user.email)


@app.get("/users", tags=['User'])
def get_all_user(token: str = Depends(oauth2_scheme)):
        return user_repository.getAll()

@app.get("/users/{id}", tags=['User'])
def get_user(id: int, token: str = Depends(oauth2_scheme)):
        return user_repository.getById(id)

@app.post("/users/create", status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(payload: UserCreate, token: str = Depends(oauth2_scheme)):
        return user_repository.create(payload)

@app.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_user(user: UserUpdate, id: int, token: str = Depends(oauth2_scheme)):
        return user_repository.update(user, id)

@app.put("/users/update-type-profile/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_type_profile_user(id: int, typeProfile: UserUpdateTypeProfile, token: str = Depends(oauth2_scheme)):
        return user_repository.updateTypeProfile(id, typeProfile)

@app.delete('/users/delete/{id}', tags=['User'])
def delete_user(id: int, token: str = Depends(oauth2_scheme)):       
        return user_repository.delete(id)


# user adm controller --------------------------------------

@app.get("/users-adm", tags=['UserAdm'])
def get_all_user_adm(token: str = Depends(oauth2_scheme)):
        return user_adm_repository.getAll()

@app.get("/users-adm/{id}", tags=['UserAdm'])
def get_user_adm(id: int, token: str = Depends(oauth2_scheme)):
        return user_adm_repository.getById(id)

@app.post("/users-adm/create", status_code=status.HTTP_201_CREATED, tags=['UserAdm'])
def create_user_adm(payload: UserAdmCreate, token: str = Depends(oauth2_scheme)):
        return user_adm_repository.create(payload)

@app.put("/users-adm/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['UserAdm'])
def update_user_adm(user: UserAdmUpdate, id: int, token: str = Depends(oauth2_scheme)):
        return user_adm_repository.update(user, id)

@app.delete('/users-adm/delete/{id}', tags=['UserAdm'])
def delete_user_adm(id: int, token: str = Depends(oauth2_scheme)):       
        return user_adm_repository.delete(id)


# portfolio controller -------------
@app.get('/portfolio/{id}', status_code=status.HTTP_200_OK, tags=['Portfolio'])
def get_by_id_portfolio(id: int, token: str = Depends(oauth2_scheme)):
        return portfolio_repository.getById(id)

@app.post('/portfolio/create', status_code=status.HTTP_201_CREATED, tags=['Portfolio'])
def create_portfolio(payload: PortfolioCreate, token: str = Depends(oauth2_scheme)):
        return portfolio_repository.create(payload)
        
        
# portfolio datas controller ------------
@app.get('/portfolio-datas', status_code=status.HTTP_200_OK, tags=['Portfolio Datas'])
def get_all_portfolio_datas(token: str = Depends(oauth2_scheme)):
        return portfolio_datas_repository.getAll()

@app.get('/portfolio-datas/{id}', status_code=status.HTTP_200_OK, tags=['Portfolio Datas'])
def get_portfolio_datas(id: int, token: str = Depends(oauth2_scheme)):
        return portfolio_datas_repository.getById(id)

@app.post('/portfolio-datas/create', status_code=status.HTTP_201_CREATED, tags=['Portfolio Datas'])
def create_portfolio_datas(payload: PortfolioDatasCreate, token: str = Depends(oauth2_scheme)):
        return portfolio_datas_repository.create(payload)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)