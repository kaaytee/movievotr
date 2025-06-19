from pydantic import BaseModel, constr, EmailStr

# --- User Schemas ---

class UserBase(BaseModel):
    """Base model for User, containing common attributes."""
    username: constr(max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class User(UserBase):
    """Schema for returning user data to the client."""
    id: int
    is_superuser: bool

    class Config:
        from_attributes = True 