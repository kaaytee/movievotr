from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """
    Test that the root endpoint returns a 200 OK status and the correct message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the MovieVotr API!"}
