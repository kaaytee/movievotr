import re
from typing import Optional
from app.models.model import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from typing import List

def get_user_by_username(username: str) -> Optional[User]:
    """
    Retrieves a user from the database by their username.
    """
    return User.get_or_none(User.username == username)

def get_user_by_email(email: str) -> Optional[User]:
    """
    Retrieves a user from the database by their email.
    """
    return User.get_or_none(User.email == email)

def create_user(user_in: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user_in.password)
    db_user = User.create(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password
    )
    return db_user

def authenticate_user(username_or_email: str, password: str) -> Optional[User]:
    """
    Authenticates a user. Returns the user object if successful, otherwise None.
    Can authenticate with either username or email.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_regex, username_or_email):
        user = get_user_by_email(email=username_or_email)
    else:
        user = get_user_by_username(username=username_or_email)
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user 


def get_user(user_id: int) -> Optional[User]:
    """
    Retrieves a user from the database by their ID.
    """
    return User.get_or_none(User.id == user_id)

def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieves a list of users with pagination.
    """
    return list(User.select().offset(skip).limit(limit))

def delete_user(user_id: int) -> Optional[User]:
    """
    Deletes a user from the database.
    """
    user = get_user(user_id=user_id)
    if user:
        user.delete_instance()
    return user
