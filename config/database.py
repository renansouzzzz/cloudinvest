from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from decouple import config

DATABASE_URL = config('DATABASE_URL')

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine('mysql://root:B1fADEdb5GaE1HFC2dC54fG3B4-AdfGb@monorail.proxy.rlwy.net:35761/railway')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()