from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Poll Option Schemas ---

class PollOptionBase(BaseModel):
    movie_details_id: int 

class PollOptionCreate(PollOptionBase):
    pass

class PollOption(PollOptionBase):
    id: int 
    suggested_by_id: int
    
    class Config:
        from_attributes = True

# --- Poll Schemas ---

class PollBase(BaseModel):
    title: str
    description: Optional[str] = None
    expires_at: Optional[datetime] = None

class PollCreate(PollBase):
    movie_ids: List[int]

class Poll(PollBase):
    id: int
    group_id: int
    creator_id: int
    is_active: bool
    options: List[PollOption] = []

    class Config:
        from_attributes = True 