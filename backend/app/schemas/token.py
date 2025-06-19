from pydantic import BaseModel
from typing import Optional

# --- Token Schemas ---

class Token(BaseModel):
    """Schema for the access token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for the data encoded within the token."""
    username: Optional[str] = None 