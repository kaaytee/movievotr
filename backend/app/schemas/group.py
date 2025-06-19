from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .user import User

# --- Group Schemas ---

class GroupBase(BaseModel):
    """Base model for Group."""
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    """Schema for creating a new group."""
    pass

class Group(GroupBase):
    """Schema for returning group data."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class GroupWithMembers(Group):
    members: List[User] 