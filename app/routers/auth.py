# router
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi import status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session
from app.database import get_db
from .. import schemas, utils, models, oauth2
router = APIRouter(
    prefix = "/login",
    tags= ["Authentication"]
)
# router path
@router.post("/", response_model=schemas.Token)
#def login(user_credential: schemas.UserLogin, db: Session= Depends(get_db)): # Use the form submission for user credential handling
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(user_credential.__dict__)
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User credential incorrect')
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User credential incorrect')
    
    token = oauth2.create_access_token(data={"user_id": user.id})

    return {"token": token, "token_type": "bearer"}


# define a login function (user credentials, database object)
# Fetch user and password
# if email not correct raise exceptions
# if password not correct raise exceptions

# return tocken