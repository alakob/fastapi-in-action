from typing import List
from fastapi import FastAPI, Response, status , HTTPException
from fastapi.params import Body, Depends
# Force the user to send data in a schema we expect.
from pydantic import BaseModel    
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm.session import Session
from starlette.status import HTTP_404_NOT_FOUND
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


while True:        
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="blaise", password="1@SSongou2", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print ("Database connection was successful")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)

app = FastAPI()
# Making use of UVCORN (an Asynchromous Server Gateway interface, lighting fast server)
@app.get("/") # Decorator for actuating path operator (root path) with HTTP operator
def root():   # Define the root application path
    return {"message": "Hello, World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts 

# The order in the API does matter.

my_post = [
    {"title" : "this is my first title", "content": "This is my first content", "id":1},
    {"title" : "this is my second title", "content": "This is my second content", "id":2},
    {"title" : "this is my third title", "content": "This is my third content", "id":3},
]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p 

def find_post_index(id):
    for index, post in enumerate(my_post):
        if post["id"] == id:
            return index 

# Create a post
@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # post = cursor.fetchall()
    # print(post)
    post = db.query(models.Post).all()
    #return {"N_post": len(my_post),"post_id": list(map(lambda x: x["id"], my_post)), "data": my_post}
    return post


# Get all the post
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # print(post.dict)
    # cursor.execute(""" INSERT INTO POST (title, content) VALUES (%s, %s) RETURNING *""", 
    # (post.title, post.content))
    # new_post  = cursor.fetchone()
    # conn.commit()
    print(post)
    print(post.dict())
    #unpaked_post = **post.dict()
    #print(unpaked_post)
    #new_post = models.Post(title = post.title, content = post.content)
    new_post = models.Post(**post.dict())
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
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session=Depends(get_db)): # We are validating the id to be an integer
    # cursor.execute(""" SELECT * FROM POSTS WHERE id=%s """,(str(id),))
    # post = cursor.fetchone() 
    # print(post)
    post = db.query(models.Post).filter(models.Post.id==id).first()   
    print(post) 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
         detail= f'Post with {id} not found')
    print(id)
    return post

# Order in path operation matters, FastAPI read from top down, 
# the first route to match the request is used eg: /posts/1 vs /post/latest
# Pay attention to the return status code, that can be checked on the postman interface and change the response from
# the code accordingly.
# Status code for delete is 204 , 
# function deleting should not return anything but a response in the form Response(status_code= status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
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
    deleted_post.delete()
    db.commit()
    #db.refresh(deleted_post)

    return Response(status_code = status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}", response_model= schemas.Post)
def update_post(id :int, post: schemas.PostCreate, db: Session = Depends(get_db)):
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

# Get all the post
@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserCreated)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    # print(post.dict)
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
@app.get("/users/{id}")
def get_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise Exception(status_code=status.HTTP_404_NOT_FOUND, details=f'User with user id {id} not found!')
    return user
