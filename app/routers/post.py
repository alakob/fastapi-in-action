from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy import func
from fastapi import FastAPI, Response, status , HTTPException, APIRouter
from fastapi.params import Body, Depends
from typing import Optional
from app.oauth2 import get_current_user

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts", 
    tags= ['Posts']
)



# Create a post
#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model = List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: Optional[int] = 10,
    search: Optional[str] ="", skip: int = 0):
    print("Alako")
    # cursor.execute(""" SELECT * FROM posts""")
    # post = cursor.fetchall()
    # print(post)
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('vote')).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
            group_by(models.Post.id).\
                filter(models.Post.title.contains(search)).\
                    limit(limit).offset(skip).all()
    #print(results.all())
    #print(results)
    #print(f'current_user_id: {current_user.id} type of current_user_id {type(current_user.id)} , type of model_user_id {dir(models.Post.id)}' )
    #post = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    print(post)
    #return {"N_post": len(my_post),"post_id": list(map(lambda x: x["id"], my_post)), "data": my_post}
    return post


# Get all the post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: str = Depends(get_current_user) ):
    print(post.dict)
    print("*"*70)
    print(dir(current_user))
    print(current_user.id)
    print(current_user.email)
    print(current_user.password)
    print("*"*70)
    # cursor.execute(""" INSERT INTO POST (title, content) VALUES (%s, %s) RETURNING *""", 
    # (post.title, post.content))
    # new_post  = cursor.fetchone()
    # conn.commit()
    print(post)
    print(post.dict())
    #unpaked_post = **post.dict()
    #print(unpaked_post)
    #new_post = models.Post(title = post.title, content = post.content)
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get post by ID

""" @app.get("/posts/{id}/")
def get_post(id: int, response: Response): # We are validating the id to be an integer
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Message": f' post with {id} not found'}
    print(id)
    print(post)
    return {"post_detail": post}
"""
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db), current_user: str = Depends(get_current_user)): # We are validating the id to be an integer
    # cursor.execute(""" SELECT * FROM POSTS WHERE id=%s """,(str(id),))
    # post = cursor.fetchone() 
    # print(post)
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label('vote')).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
            group_by(models.Post.id).filter(models.Post.id==id).first()   
    print(post) 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
         detail= f'Post with {id} not found')
    #if post.user_id != current_user.id:
    #      raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform requested action')
    #print(id)
    return post

# Order in path operation matters, FastAPI read from top down, 
# the first route to match the request is used eg: /posts/1 vs /post/latest
# Pay attention to the return status code, that can be checked on the postman interface and change the response from
# the code accordingly.
# Status code for delete is 204 , 
# function deleting should not return anything but a response in the form Response(status_code= status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # find index of the post to delete_post
    # Post the index from the list
    # cursor.execute(""" DELETE FROM POSTS WHERE id=%s RETURNING *""", (str(id),) )
    # deleted_post = cursor.fetchone()
    # print(deleted_post)
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id ==id)
    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail=f"Post with id {id} not found")
    if current_user.id != deleted_post.first().user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f'Unauthorized action')
    deleted_post.delete()
    db.commit()
    #db.refresh(deleted_post)

    return Response(status_code = status.HTTP_204_NO_CONTENT)




@router.put("/{id}", response_model= schemas.Post)
def update_post(id :int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user) ):
    #index = find_post_index(id)
    # cursor.execute(""" UPDATE POSTS SET title=%s, content=%s WHERE id=%s RETURNING *""", 
    # (post.title, post.content,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_result = post_query.first()
    if post_result == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f'Post with id {id} is not found')
    if current_user.id != post_result.user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f'Unauthorized action')
    post_query.update(post.dict())
    db.commit()
    #post = post.dict()
    #post["id"] = id # Make sure to add the id in the dictionary..
    #my_post[index]  = post
    print(post) 
    return post_query.first()

# After creating the CRUD methods. Lets structure the code directory by creating an app folder and move main.py therein.
# add __init__py in app folder to turn it into a python package.

# PostgreSQL database.
# Create a user and database in postgres
# sudo su - postgres
# postgres@dreamBig-T7920:~$ psql
# postgres=# CREATE USER blaise with PASSWORD '1@SSongou2';
# CREATE ROLE
# postgres=# CREATE DATABASE fastapi;
# CREATE DATABASE
# postgres=# GRANT ALL PRIVILEGES ON DATABASE fastapi to blaise;
# GRANT
# postgres=# \q
# Modify the client authentication file sudo vim /etc/postgresql/12/main/pg_hba.conf
# To use MD5 method

# Move the pydantic model to a schemas.py file

# Make some clean up

# Define a schema for the response content.

