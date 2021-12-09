# Create access token using the jwt package. (needed)
# data (payload) + SECRET_TOKEN + TOKEN_EXPIRATION_TIME + ALGORITHM


from datetime import datetime, timedelta
from fastapi.params import Depends
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session


from app.database import get_db
from . import schemas, models
from fastapi import HTTPException, status 
from fastapi.security import OAuth2PasswordBearer

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_TOKEN = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRATION_TIME = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp" : expire})
    print(to_encode)
    access_token = jwt.encode(to_encode, SECRET_TOKEN, algorithm = ALGORITHM)
    #return {"token" : access_token, "token_type" : "bearer"}
    return access_token

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        print(payload)
        print(user_id)
        if user_id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id = user_id)
        print(token_data)
    except JWTError as error:
        print(error)
        raise credentials_exceptions
    return token_data

# Return the user email from the database
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db) ): # force user  authentication
    print(token)
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f'Unauthorized credentials provided', 
    headers={"WWW-Authenticate" : "Bearer"})
    token =  verify_access_token(token, credential_exceptions)
    email = db.query(models.User).filter(models.User.id == token.id).first()
    print(f'email {dir(email)}')
    return email
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# # Secret key
# # Algorithm
# # Expiration date
# # update data dict with expiration date
# # Encode data + secret + algorithm with jwt.encode

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def create_access_token (data : dict):
#     to_encode = data.copy()
#     expire = datetime.now() - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # Encode the data. oauth from fastapi
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return {"token": encoded_jwt, "token_type": "bearer"}

