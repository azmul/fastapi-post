from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from hashing import Hash

import models, schemas, database

router = APIRouter()

db_dependency = Annotated[Session, Depends(database.get_db)]

# CREATE User
@router.post("/users", status_code=status.HTTP_201_CREATED, tags=['User'])
async def create_user(user: schemas.UserBase, db: db_dependency):
    new_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    db.add(new_user)   
    db.commit()
    db.refresh(new_user)
    return new_user

# GET User by ID
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUserBase, tags=['User'])
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user