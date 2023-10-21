from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from typing import Annotated
from database import engine, SessionLocal
from schemas import PostBase, UserBase, SHowPostBase, ShowUserBase
from hashing import Hash

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


# CREATE User
@app.post("/users", status_code=status.HTTP_201_CREATED, tags=['User'])
async def create_user(user: UserBase, db: db_dependency):
    new_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    db.add(new_user)   
    db.commit()
    db.refresh(new_user)
    return new_user

# GET User by ID
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUserBase, tags=['User'])
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# CREATE Post
@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['Blog'])
async def create_post(post: PostBase, db: db_dependency):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

# GET All Post
@app.get("/posts", status_code=status.HTTP_200_OK, response_model=list[SHowPostBase], tags=['Blog'])
async def read_all_posts(db: db_dependency):
    posts = db.query(models.Post).all()
    return posts
   
# GET Post by ID 
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=SHowPostBase, tags=['Blog'])
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# UPDATE Post by ID 
@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
async def update_post(post_id:int, post: PostBase, db: db_dependency): 
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.update(post.dict())
    db.commit()
    return "Updated" 

# DELETE Post by ID 
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
async def delete_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return post