from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(prefix="/event", tags=["Events"])

# Create
# should be an Admin work
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db),  current_user=Depends(oauth2.get_current_user)):
    new_event = models.Event(creator_id= current_user.id, **event.dict())
# 
    organizing_society = db.query(models.Society).filter(models.Society.name == new_event.organized_by).first()
    if not organizing_society:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The society with name {new_event.organized_by} does not exist") 
#
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# Read
@router.get("", response_model=List[schemas.EventOut])
def get_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    return events

# Read
@router.get("/{id}", status_code = status.HTTP_302_FOUND, response_model=schemas.EventOut)
def get_event_by_id(id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == id).first() 
    
    if not event:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Society with id {id} not found")

    return event

# Update
@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.EventCreate)
def update_event(id: int, updated_event: schemas.EventCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    event_query = db.query(models.Event).filter(models.Event.id == id)

    event = event_query.first()

    if not event:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Society with id {id} not found")

    if event.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"Not authorized to perform the operation")
    
    event_query.update(updated_event.dict(), synchronize_session=False)
    db.commit()
    db.refresh(event)
    
    return event

# Admin work
# Delete
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_event(id: int, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    event_query = db.query(models.Society).filter(models.Society.id == id)
    event = event_query.first()

    if not event:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found.")
    
    if event.creator_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to performm the requested action")

    event_query.delete(synchronize_session="fetch")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
