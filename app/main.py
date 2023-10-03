from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status,Depends
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import utils
from app.routers.user import UserCreate, userReponse
from . import models
from .models import Post
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from .routers import user,auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.DATABASE_PASSWORD)



# from passlib .context import CryptContext

# # what is the hashing algorithim we gonna use 
# pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# provide the list of all public URL that our API's can communicate each other 
origins = ["https://www.google.com"] 
app.add_middleware(
    CORSMiddleware,
    # we are allowing on what domains our API can be hit 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Posts(BaseModel):
    # id : int
    title : str 
    content : str 
    # published: bool = True
    # created_at : Optional[int] = None
    
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# test for sql alchemy 

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    new_post = db.query(models.Post).all()
    print(new_post)
    return {"status": new_post}

# @app.get("/posts")
# def getAllposts(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     print(post)
#     return {"data":post}


# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def publishintodatabse(post : models.Post,db: Session = Depends(get_db)):
#     # cursor.execute(""" insert into products (name,id,price,is_sale) values(%s,%s,%s,%s) RETURNING * """,(product.name,product.id,product.price,product.is_sale))
#     # new_product = cursor.fetchone()
#     # conn.commit()
#     new_post = models.Post(id=post.id,title=post.title,content=post.content,published=post.published)
#     # pydantic_post = PostResponse(id=new_post.id, title=new_post.title, content=new_post.content, published=new_post.published)

#     return {"data" : new_post } 

# update the posts in the databse  
# @app.put("/updateposts/{id}", response_model=Post)
# def update_post(id: int, post: Post, db: Session = Depends(get_db)):
#     # Check if the post with the given id exists
#     existing_post = db.query(models.Post).filter(models.Post.id == id).first()

#     if existing_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

#     # Update the post's title and content
#     db.query(models.Post).filter(models.Post.id == id).update(
#         {"title": 'this is the updated title', 'content': 'this is updated content'},
#         synchronize_session=False
#     )

#     db.commit()

#     return {"data": "successful"}


class Product(BaseModel): 
    name : str 
    id : int 
    price : int 
    is_sale: bool

# loop tilll we get the successful connection it is used for the case where we have problem with the connection code 

while True:
    try:
        conn = psycopg2.connect(host ='localhost',database = 'FastAPI',user='postgres',password = 'mudit1995',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Databse connection was successful')
        break
    except Exception as error:
        print('connection failed')
        print("error:-",error)    
        time.sleep(2)

#first thing we gonna get all the post present in the table product table 
@app.get("/posts")
def getAllposts():
    posts = cursor.execute(""" select * from products   """)
    posts = cursor.fetchall()
    print(posts)
    return {"data":posts}

# publish a report from the client and save it into the database 
@app.post("/products", status_code=status.HTTP_201_CREATED)
def publishintodatabse(product : Product):
    cursor.execute(""" insert into products (name,id,price,is_sale) values(%s,%s,%s,%s) RETURNING * """,(product.name,product.id,product.price,product.is_sale))
    new_product = cursor.fetchone()
    conn.commit()
    return {"data" : product } 

## get one post based ont he id  
# @app.get("/products/{id}")
# def getsinglepost(id:int, response: Response):
#     cursor.execute(""" select * from products where id = %s """,(str(id)))
#     test_product = cursor.fetchone()
#     print(test_product)
#     if not test_product : 
#         response.status_code = status.HTTP_404_NOT_FOUND
#     return {"postdetails":test_product}


@app.get("/")
def root():
    return {"message":"hello world 12 3qqqqq 4 5 6q 7"}

@app.get("/posts")
def GetPosts():
    return {"data":"this is your posts"}

@app.post("/CreatePosts")
def CreatePosts():
    return {"message":"succesfully created posts"}

# @app.post("/SaveDataToServer")
# def CreatePosts(p: dict = Body(...)):
#     print(p)
#     return {"message":"succesfully created posts"}

# forcing the front end users to send the data in a particular schema that we want them so we need to validate the data for sending the request 
#title: str 
#content : Str  

# # a class which will gona lool like whhat are model should look like that means what are the data that we want 

my_post = [{"title":"title of post 1",
             "content" : "content of post 1",
             "id" : 1
             }, {"title":"favourite food",
             "content" : "I like pizza",
             "id" : 2} ] 
  



@app.get("/posts")
def GetPosts():
    return {"data": "my_post"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def CreatePosts(newPost : Posts):
    post_dict = newPost.dict()
    x=randrange(3,100000)
    post_dict['id']  = x
    my_post.append(post_dict)
    # print(newPost.rating)
    # print(newPost.dict())
    print(my_post)
    print(x)
    # print(my_post[])
    print(my_post[-1])
    return {"data":post_dict}

# path paremiter for the single posts
@app.get("/posts/{id}")
def getsinglepost(id:int, response: Response):
    
    post = find_post(id)
    if not post : 
        response.status_code = status.HTTP_404_NOT_FOUND
    print(post)
    return {"postdetails":f"here is post{id}"}


def find_post(id):
    for p in my_post :
        if p["id"] == id : 
            return p


@app.delete("/posts/{id}")
def deletePost(id:int):
    #deleting a post 
    #find the index in tehe array that has the required ID  
    #my_posts.pop(index)
    print(id)
    index = find_post(id)
    print(index)
    # my_post.pop(index)
    return {"message" : "successfully deleted the post"}

def find_index(id):
    for i,p in enumerate(my_post):
        if p['id'] == id : 
            return i


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

