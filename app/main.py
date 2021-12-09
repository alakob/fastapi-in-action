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
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Making use of UVCORN (an Asynchromous Server Gateway interface, lighting fast server)
@app.get("/") # Decorator for actuating path operator (root path) with HTTP operator
def root():   # Define the root application path
    return {"message": "Hello, World"}




# while True:        
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="blaise", password="1@SSongou2", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print ("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(2)


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts 

# The order in the API does matter.

# my_post = [
#     {"title" : "this is my first title", "content": "This is my first content", "id":1},
#     {"title" : "this is my second title", "content": "This is my second content", "id":2},
#     {"title" : "this is my third title", "content": "This is my third content", "id":3},
# ]

# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p 

# def find_post_index(id):
#     for index, post in enumerate(my_post):
#         if post["id"] == id:
#             return index 


