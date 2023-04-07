from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, ARRAY
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base



class Society(Base):
    __tablename__ = "societies"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    college_level = Column(Boolean, nullable=False, server_default='False') 
    convenor = Column(String, nullable=False)
    gen_sec = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    events = relationship("Event", back_populates = "organizer")
    


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    organized_by = Column(String, ForeignKey('societies.name', ondelete='Cascade'), nullable=False)
    event_time = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="Cascade"), nullable=False)
    # organizer_team_ids = Column(ARRAY(Integer), nullable=False)
    creator = relationship("User")
    organizer = relationship("Society", back_populates = "events")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    email_id = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    college_roll_no = Column(Integer, nullable=False, unique=True)
    # mobile_num = Column(Integer, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

