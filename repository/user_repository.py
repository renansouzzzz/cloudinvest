from MySQLdb import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import UserCreate, UserUpdate, TypeProfileEnumDTO, UserUpdateTypeProfile
from schemas.user import UserMapped, UserSchema, UserSchema

from config.database import engine
from cryptography.fernet import Fernet, InvalidToken

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

key = Fernet.generate_key()
fernet = Fernet(key)


def getAll():
    with Session(engine) as session:
        data = session.query(UserMapped).all()
        if data is None:
            raise ValueError(f'Nenhum usuário encontrado!')
        return data

def getById(id: int):
    with Session(engine) as session:
        data = session.get(UserMapped, id)
        data.password = fernet.decrypt(data.password).decode()
        
        if data is None:
            raise ValueError(f'O usuário com ID {id} não foi encontrado!')
        
        return data
    
def getByIds(id: int):
    with Session(engine) as session:
        data = session.get(UserMapped, id)
        data.password = fernet.decrypt(data.password).decode()
        
        if data is None:
            raise ValueError(f'O usuário com ID {id} não foi encontrado!')
        
        return data
    
def getByEmail(email):
    with Session(engine) as session:
        user = session.query(UserSchema).filter(UserSchema.email == email).first()
        if user is None:
            raise ValueError(f'O usuário com email {email} não foi encontrado!')

        try:
            user.password = fernet.decrypt(user.password).decode()
        except InvalidToken:
            raise ValueError('Erro ao descriptografar a senha. A senha pode estar incorreta ou corrompida.')

        return user

def create(payload: UserCreate):
    with Session(engine) as session:
        
        user = UserSchema(**payload.dict())
        
        
        user.password = fernet.encrypt(user.password.encode())
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user


def update(user: UserUpdate, id: int):
    with Session(engine) as session:
        try:
            getUserById = session.query(UserSchema).filter(UserSchema.id == id).one_or_none()
            
            if not getUserById:
                raise HTTPException(status_code=404, detail="Usuário não encontrado!")
            
            for var, value in vars(user).items():
                setattr(getUserById, var, value)
                
            session.add(getUserById)
            session.commit()
            session.refresh(getUserById)
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')
        
        return getUserById
    
def updateTypeProfile(id: int, user: UserUpdateTypeProfile):
    with Session(engine) as session:
        
        try:
            getUserById = session.query(UserMapped).filter(UserMapped.id == id).one_or_none()
            
            if not getUserById:
                raise HTTPException(status_code=404, detail="Usuário não encontrado!")
            
            if user.type_profile not in TypeProfileEnumDTO:
                raise HTTPException(status_code=404, detail="Tipo de perfil não existente!")
            
            getUserById.type_profile = user.type_profile
            session.commit()
            session.refresh(getUserById)
        
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')
        
        return "Perfil de usuário atualizado com sucesso!"
    
    """
    _delete apenas desativa o campo ACTIVE_
    """
def delete(id: int):
    with Session(engine) as session:
        try:
            getUser = session.get(UserSchema, id)
            
            if not getUser:
                raise HTTPException(status_code=404, detail="Usuário não encontrado!")
            
            session.execute(f"UPDATE user SET active = false WHERE id = {id}")
            session.commit()     
        
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f'Error on database: {e}')
        
        return "Deletado com sucesso!"    