from fastapi import status, Response, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/user", tags=["Users"])


# Read/fetch
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")

    return user


# Create
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())
    new_user.display_name = new_user.display_name.lower()

    check_user_email = db.query(models.User).filter(
        models.User.email_id == new_user.email_id).first()
    check_user_college_roll_no = db.query(models.User).filter(
        models.User.college_roll_no == new_user.college_roll_no).first()
    check_user_display_name = db.query(models.User).filter(
        models.User.display_name == new_user.display_name).first()

    if check_user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email {new_user.email_id} already exists.")

    if check_user_college_roll_no:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with roll no. {new_user.college_roll_no} already exists.")

    if check_user_display_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with display_name. {new_user.display_name} already exists.")

    # Hash user_password
    new_user.password = utils.hash(user.password)
    # new_user.display_name
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
