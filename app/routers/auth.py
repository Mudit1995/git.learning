from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, models, utils, outh
from .user import USerLogin
from ..database import engine,SessionLocal
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post('/login')
def login(user_crediatnials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    { 
        "username" : "jhvva", 
        "password" : "vva"
    }
    
    # just declaring two varibales in a dictinary because during the postman request we will gonna send the userbame and password 
     # oaOAuth2PasswordRequestForm will gonna retunr two things username and password 
    user = db.query(models.User).filter(models.User.email == user_crediatnials.username).first() 
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Crediantls")
    
    if not utils.verify(user_crediatnials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid crediatls")
    
    # create a token and retunr a token 

    access_token=outh.create_access_token(data={"user_id":user.id})
    return {"acess_token" : access_token, "token_type" : "bearer"}
    

