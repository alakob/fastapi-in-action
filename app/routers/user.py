from typing import List
from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Response, status , HTTPException, APIRouter
from fastapi.params import Body, Depends

from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags= ['Users']
)


# Get all the post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserCreated)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    print(user.dict)
    # cursor.execute(""" INSERT INTO POST (title, content) VALUES (%s, %s) RETURNING *""", 
    # (post.title, post.content))
    # new_post  = cursor.fetchone()
    # conn.commit()
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    print(user)
    print(user.dict())
    #unpaked_post = **post.dict()
    #print(unpaked_post)
    #new_post = models.Post(title = post.title, content = post.content)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    #db.refresh(new_user)
    return new_user

# Now it is time to hash the user password with JWT 
# (install passlib and Bcrypt: pip install passlib[bcrypt])

# Create a path operation for getting user profiles
@router.get("/{id}")
def get_user(id: int, db: Session= Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user.dict)
    if not user:
        raise Exception(status_code=status.HTTP_404_NOT_FOUND, details=f'User with user id {id} not found!')
    return user
