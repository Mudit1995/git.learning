from pydantic import BaseModel, EmailStr
from .. import models, utils
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import engine,SessionLocal
from sqlalchemy.orm import Session
from .. import models,utils
from ..models import Post
from app import models
from typing import Optional, List
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
##### ceating the user 
# we will gonna add a new schema to it 
class UserCreate(BaseModel):
    email : str 
    password : str 

class userReponse(BaseModel):
    id:int 
    email:str 

    class Config:
        orm_mode = True

class USerLogin(BaseModel):
    email: EmailStr
    password:str 

class token(BaseModel):
    accesstoekn : str 
    token_type : str 

class TokenData(BaseModel):
    id: Optional[str] = None

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=userReponse)
def create_user( user: UserCreate, db:Session = Depends(get_db)):
    # hash the password - user.password  
    # user_hashed_password = pwd_context.hash(user.password)
    user_hashed_password = utils.hash(user.password)
    user.password = user_hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.get('/users/{id}',response_model=userReponse)
def getUser(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
