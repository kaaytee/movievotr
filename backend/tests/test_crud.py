from app.crud.crud_user import create_user, get_user_by_username
from app.schemas.user import UserCreate


def test_create_and_get_user(test_db):
    user_in = UserCreate(username="testuser", email="test@example.com", password="testpassword")
    db_user = create_user(user_in=user_in)

    assert db_user.username == user_in.username
    assert db_user.email == user_in.email

    retrieved_user = get_user_by_username(username=user_in.username)
    assert retrieved_user
    assert retrieved_user.username == user_in.username
