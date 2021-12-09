from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from pydantic.networks import EmailStr
from pydantic.types import conint


# CRUD create(post), Read(get), Update(put/patch), Delete(delete) (path operations are in plurals (e.g /posts))


class UserCreated(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase):
    id : int
    created_at: datetime
    user_id: int
    user: UserOut

    #pass
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    vote: int
    
    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    #expires: Optional[datetime]
    id: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)