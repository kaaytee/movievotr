import jwt
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password

def test_password_hashing_and_verification():
    """
    Tests that password hashing and verification work correctly.
    """
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)

    assert password != hashed_password

    assert verify_password(password, hashed_password) is True

    assert verify_password("wrongpassword", hashed_password) is False


def test_create_access_token():
    """
    Tests that a JWT access token is created correctly.
    """
    user_data = {"sub": "testuser@example.com"}
    token = create_access_token(data=user_data)

    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded_token["sub"] == user_data["sub"]
