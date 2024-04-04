from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from decouple import config

# DATABASE_URL = config('DATABASE_URL')

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine('mysql://root:PtAxspmdLRVqaMeCxdztmZEqLgItwvGD@viaduct.proxy.rlwy.net:20004/railway')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
