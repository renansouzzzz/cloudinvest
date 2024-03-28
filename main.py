from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

from models.user import UserCreate, UserUpdate, UserUpdateTypeProfile
from models.user_adm import UserAdmCreate, UserAdmUpdate
from models.portfolio_datas import PortfolioDatasCreate
from models.token_data import TokenData

from config.database import Base, engine
from repository import user_repository, user_adm_repository, portfolio_datas_repository

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from security.token.token_verify import Token

from security.user_security.security_verify import authenticate_user

origins = [
    "*",
]

app = FastAPI(
        title='PLANE LIFE - FastAPI -> ReactNative'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/", tags=['Health check'])
async def read_root():
    return {"message": "API EXECUTADA COM SUCESSO!"}


@app.post("/token", tags=['Token'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário ou senha inválidos',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        
    access_token = Token.create_access_token(user.email)
    
    userData = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'active': user.active,
        'type_profile': user.type_profile
    }
        
    return TokenData(access_token=access_token, user=userData)


@app.get("/logout/", tags=['Logout'])
async def logout(token: str = Depends(oauth2_scheme)):
    token_data = Token.verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {"message": "Logout realizado com sucesso"}


@app.get("/users", tags=['User'])
def get_all_user(token: str = Depends(oauth2_scheme)):
        try:
                return user_repository.getAll()
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.get("/users/{id}", tags=['User'])
def get_user(id: int, token: str = Depends(oauth2_scheme)):
        try:
                return user_repository.getById(id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')
        

@app.post("/users/create", status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(payload: UserCreate):
        try:
                return user_repository.create(payload)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_user(user: UserUpdate, id: int, token: str = Depends(oauth2_scheme)):
        try:
                return user_repository.update(user, id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.put("/users/update-type-profile/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['User'])
def update_type_profile_user(id: int, typeProfile: UserUpdateTypeProfile, token: str = Depends(oauth2_scheme)):
        try:
                return user_repository.updateTypeProfile(id, typeProfile)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.delete('/users/delete/{id}', tags=['User'])
def delete_user(id: int, token: str = Depends(oauth2_scheme)): 
        try:      
                return user_repository.delete(id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')


# user adm controller --------------------------------------

@app.get("/users-adm", tags=['UserAdm'])
def get_all_user_adm(token: str = Depends(oauth2_scheme)):
        try:
                return user_adm_repository.getAll()
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.get("/users-adm/{id}", tags=['UserAdm'])
def get_user_adm(id: int, token: str = Depends(oauth2_scheme)):
        try:
                return user_adm_repository.getById(id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')
        
@app.post("/users-adm/create", status_code=status.HTTP_201_CREATED, tags=['UserAdm'])
def create_user_adm(payload: UserAdmCreate, token: str = Depends(oauth2_scheme)):
        try:
                return user_adm_repository.create(payload)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')
        
@app.put("/users-adm/update/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['UserAdm'])
def update_user_adm(user: UserAdmUpdate, id: int, token: str = Depends(oauth2_scheme)):
        try:
                return user_adm_repository.update(user, id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.delete('/users-adm/delete/{id}', tags=['UserAdm'])
def delete_user_adm(id: int, token: str = Depends(oauth2_scheme)):
        try:     
                return user_adm_repository.delete(id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

        
# portfolio datas controller ------------
@app.get('/portfolio-datas/user/{idUser}', status_code=status.HTTP_200_OK, tags=['Portfolio Datas'])
def get_all_by_user_portfolio_datas(idUser: int, token: str = Depends(oauth2_scheme)):
        try:
                return portfolio_datas_repository.getAll(idUser)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.get('/portfolio-datas/{id}', status_code=status.HTTP_200_OK, tags=['Portfolio Datas'])
def get_portfolio_datas(id: int, token: str = Depends(oauth2_scheme)):
        try:
                return portfolio_datas_repository.getById(id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.post('/portfolio-datas/create', status_code=status.HTTP_201_CREATED, tags=['Portfolio Datas'])
def create_portfolio_datas(payload: PortfolioDatasCreate, token: str = Depends(oauth2_scheme)):
        try:
                return portfolio_datas_repository.create(payload)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.delete('/portfolio-datas/delete', status_code=status.HTTP_202_ACCEPTED, tags=['Portfolio Datas'])
def delete_portfolio_datas(id: int, token: str = Depends(oauth2_scheme)):
        try:
                return portfolio_datas_repository.delete(id)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@app.get('/portfolio-datas/get-by-date/{idUser}', status_code=status.HTTP_202_ACCEPTED, tags=['Portfolio Datas'])
def get_by_date_portfolio_datas(idUser: int, month: str, year: int, token: str = Depends(oauth2_scheme)):
        try:
                return portfolio_datas_repository.getByDate(idUser, month, year)
        except ValueError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')        
        

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)