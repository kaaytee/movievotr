from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, crud, models
from app.api import deps
from app.core.security import create_access_token
from app.api.deps import bearer_scheme

router = APIRouter()

@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate):
    """
    Create a new user and return an access token.
    """
    user_by_username = crud.crud_user.get_user_by_username(username=user_in.username)
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user_by_email = crud.crud_user.get_user_by_email(email=user_in.email)
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = crud.crud_user.create_user(user_in=user_in)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# 
@router.post("/login", response_model=schemas.Token)
def login_with_username_or_email(username_or_email: str, password: str ):
    """
    Authenticate user and return a JWT access token.
    """
    user = crud.crud_user.authenticate_user(
        username_or_email=username_or_email, password=password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# OAuth2 Password Flow
@router.post("/loginOAuth", response_model=schemas.Token)
def login_for_access_tokenOAuth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return a JWT access token.
    """
    user = crud.crud_user.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    """
    Get the current logged-in user's details.
    """
    return current_user 

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, current_user: models.User = Depends(deps.get_current_user)):
    """
    Get a user by their ID.
    """
    user = crud.crud_user.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user")
    return user