from pydantic import BaseModel

# --- Vote Schemas ---

class VoteCreate(BaseModel):
    """Schema for casting a vote."""
    poll_option_id: int

class Vote(BaseModel):
    """Schema for displaying a vote."""
    poll_option_id: int
    voter_id: int
    
    class Config:
        from_attributes = True 