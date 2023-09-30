from jose import JWTError, jwt
from datetime import datetime, timedelta

from pydantic import BaseModel
from . import  database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from typing import Optional


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# creating the tokens we require 1 thing 
# 1. seceret key and this key willl reisde to the server only 
# 2. provide the algorithim to be used -- SH 256 
# 3. Expiration time  


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
# expiration time for JWT 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    encoded_data = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp":expire})

    ecoded_jwt = jwt.encode(encoded_data,SECRET_KEY,algorithm = ALGORITHM)

    return ecoded_jwt

# def verify_access_toekn(token:str, credentials_exception):
#     payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)

# id : str = payload.get("user_id")

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
