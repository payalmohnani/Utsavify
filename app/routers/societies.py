from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from .. import models, schemas


router = APIRouter(prefix="/society", tags=["Societies"])

# Create
# should be an Admin work
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.SocietyOut)
def create_society(society: schemas.SocietyCreate, db: Session = Depends(get_db)):
    new_society = models.Society(**society.dict())

    # name already in db

    existing_society = db.query(models.Society).filter(func.lower(models.Society.name) == func.lower(new_society.name)).first()

    # print(existing_society,"\n\n")
    if existing_society:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"Society with the name {new_society.name} already exists. Try using a different name.")

    db.add(new_society)
    db.commit()
    db.refresh(new_society)
    return new_society

# Read
@router.get("", response_model=List[schemas.SocietyOut])
def get_society(db: Session = Depends(get_db)):
    societies = db.query(models.Society).all()
    return societies

# Read
@router.get("/{id}", status_code = status.HTTP_302_FOUND, response_model=schemas.SocietyOut)
def get_society_by_id(id: int, db: Session = Depends(get_db)):
    society = db.query(models.Society).filter(models.Society.id == id).first() 
    
    if not society:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Society with id {id} not found")

    return society

# Update
@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.SocietyOut)
def update_society(id: int, updated_society: schemas.SocietyCreate, db: Session = Depends(get_db)):

    society_query = db.query(models.Society).filter(models.Society.id == id)

    society = society_query.first()

    if not society:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Society with id {id} not found")

    # Restricting society name change
    if str(society.name).lower() != str(updated_society.name).lower():
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail="Name of the society cannot be changed")
    
    updated_society.name = society.name
    society_query.update(updated_society.dict(), synchronize_session=False)
    db.commit()
    db.refresh(society)
    
    return society

# Admin work
# Delete
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_society(id: int, db : Session = Depends(get_db)):
    
    society_query = db.query(models.Society).filter(models.Society.id == id)
    society = society_query.first()

    if not society:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found.")
    
    society_query.delete(synchronize_session="fetch")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
