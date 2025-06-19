from pydantic import BaseModel
from typing import Optional

# --- Movie Schemas ---

class MovieBase(BaseModel):
    """Base model for Movie."""
    tmdb_id: str
    title: str
    release_year: Optional[int] = None
    poster_url: Optional[str] = None

class MovieCreate(MovieBase):
    """Schema for creating a movie in our catalog."""
    pass

class Movie(MovieBase):
    """Schema for returning movie data from our catalog."""
    id: int

    class Config:
        from_attributes = True 