from typing import Optional
from fastapi import FastAPI, Response, status , HTTPException
from fastapi.params import Body
# Force the user to send data in a schema we expect.
from pydantic import BaseModel    
from random import randrange

# CRUD create(post), Read(get), Update(put/patch), Delete(delete) (path operations are in plurals (e.g /posts))
class Post(BaseModel):
    title : str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()
# Making use of UVCORN (an Asynchromous Server Gateway interface, lighting fast server)
@app.get("/") # Decorator for actuating path operator (root path) with HTTP operator
def root():   # Define the root application path
    return {"message": "Hello, World"}

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
@app.get("/posts")
def get_post():
    #return {"N_post": len(my_post),"post_id": list(map(lambda x: x["id"], my_post)), "data": my_post}
    return {"data": my_post}


# Get all the post
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post)
    print(post.json()) 
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(1,1000000)
    my_post.append(post_dict)
    return {"new_post" : post_dict}

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
@app.get("/posts/{id}/")
def get_post(id: int): # We are validating the id to be an integer
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
         detail= f'Post with {id} not found')
    print(id)
    print(post)
    return {"post_detail": post}

# Order in path operation matters, FastAPI read from top down, 
# the first route to match the request is used eg: /posts/1 vs /post/latest
# Pay attention to the return status code, that can be checked on the postman interface and change the response from
# the code accordingly.
# Status code for delete is 204 , 
# function deleting should not return anything but a response in the form Response(status_code= status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index of the post to delete_post
    # Post the index from the list
    index  = find_post_index(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail=f"Post with id {id} not found")
    my_post.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id :int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f'Post with id {id} is not found')
    post = post.dict()
    post["id"] = id # Make sure to add the id in the dictionary..
    my_post[index]  = post
    print(post) 
    return {"data": post}

# After creating the CRUD methods. Lets structure the code directory by creating an app folder and move main.py therein.
# add __init__py in app folder to turn it into a python package.