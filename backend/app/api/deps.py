from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.core.config import settings
from app.schemas.token import TokenData
from app.crud import crud_user
from app.models.model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


# swagger auth
def get_current_user(
    token_from_oauth: Optional[str] = Depends(oauth2_scheme),
    creds_from_bearer: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> User:
    """
    1. OAuth2 Password Flow (username/password)
    2. jwt
    
    Raises HTTPException if the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token: Optional[str] = None
    if token_from_oauth:
        token = token_from_oauth
    elif creds_from_bearer:
        token = creds_from_bearer.credentials

    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = crud_user.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user