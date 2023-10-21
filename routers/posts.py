from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

import models, schemas, database

router = APIRouter()

db_dependency = Annotated[Session, Depends(database.get_db)]

# CREATE Post
@router.post("/posts", status_code=status.HTTP_201_CREATED, tags=['Blog'])
async def create_post(post: schemas.PostBase, db: db_dependency):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

# GET All Post
@router.get("/posts", status_code=status.HTTP_200_OK, response_model=list[schemas.SHowPostBase], tags=['Blog'])
async def read_all_posts(db: db_dependency):
    posts = db.query(models.Post).all()
    return posts
   
# GET Post by ID 
@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.SHowPostBase, tags=['Blog'])
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# UPDATE Post by ID 
@router.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
async def update_post(post_id:int, post: schemas.PostBase, db: db_dependency): 
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.update(post.dict())
    db.commit()
    return "Updated" 

# DELETE Post by ID 
@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
async def delete_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return post