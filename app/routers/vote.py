

from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi import status
from sqlalchemy.orm.session import Session
from fastapi import Depends
from  .. import database, models, schemas, oauth2

router  = APIRouter(prefix="/votes", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_user)):
    print(dir(current_user))
    # Raise an edxception if a post does not exists.
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {vote.post_id} not found')
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    new_vote = vote_query.first()
    if vote.dir ==1 :
        if new_vote:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f'User {current_user.id} already voted for this post {vote.post_id}')
        db.add(models.Vote(post_id = vote.post_id, user_id=current_user.id))
        db.commit()
        return {"Message": "Post successfully voted"}
    else:
        if not new_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no post found')
        vote_query.delete()
        db.commit()    
        return {"Message" : f'Post {vote.post_id} successully deleted'}

