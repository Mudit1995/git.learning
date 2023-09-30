from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings 

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:mudit1995@localhost/FastAPI'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:mudit1995@localhost/FastAPI'

# this URL we need to add the custom made URL that parameters like postgresSQL/ mudit1995@localhost/FastAPI 
# we need to add the enviroment variable where we will not hard core parametrs instead we will pass the values to the environment variable so that it cannot be hard coded
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

# engine to connect with the sqlalchemy with the pytohn app 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# when we are talkiong to the database we gonna use the seesion 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
