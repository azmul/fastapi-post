from __future__ import annotations
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    
class ShowPostUserBase(BaseModel):
    name: str
    email: str

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    
class ShowUserBase(BaseModel):
    id: int
    name: str
    email: str
    posts: list[PostBase]
    
class SHowPostBase(BaseModel):
    title: str
    content: str
    user: ShowPostUserBase
    
class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None