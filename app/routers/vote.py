from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from pydantic import BaseModel, EmailStr, conint
from .. import database, models, outh
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags = ['Vote'] 
)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Vote(BaseModel): 
    post_id : int 
    dir:conint(le=1)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:Vote, db:Session = Depends(get_db), current_user : int = Depends(outh.get_current_user)): 
    vote_querry = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_querry.first()

   
    if (vote.dir == 1):
        # if vote aready exists or not  
        if found_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, details = "Current user has laready linked the post ")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added vote"}
    else: 
        if not found_vote: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details= "Vote doe snot exist")
        vote_querry.delete(synchronize_session=False)
        db.commit()
        return {"message":"succesfully deleted vote"}


    