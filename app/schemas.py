from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Schemas for Society
class SocietyBase(BaseModel):
    name : str
    college_level : bool
    convenor : str
    gen_sec : str

class Society(SocietyBase):
    id : int
    created_at : datetime
    class Config:
        orm_made = True 

class SocietyCreate(SocietyBase):
    class Config:
        orm_made = True 

class SocietyOut(Society):
    class Config:
        orm_mode = True


# Schemas for Events
class EventBase(BaseModel):
    name : str
    organized_by : str
    event_time : datetime
    

class Event(EventBase):
    id : int
    created_at : datetime
    class Config:
        orm_made = True 

class EventCreate(EventBase):
    class Config:
        orm_made = True 

class EventOut(Event):
    class Config:
        orm_mode = True

# Schemas for users
class UserBase(BaseModel):
    first_name : str
    last_name : str
    email_id: EmailStr    
    display_name : str


class UserCreate(UserBase):
    password: str
    college_roll_no : int

    class Config:
        orm_mode = True

class UserOut(UserBase):
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email_id: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None
