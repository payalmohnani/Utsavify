from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email_id == user_credentials.username.lower()).first() 

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    

    access_token = oauth2.create_access_token(data={"current_user": user.id})

    return {"access_token": access_token, "token_type": "bearer"}