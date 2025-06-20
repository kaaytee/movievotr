import pytest
from fastapi.testclient import TestClient

from app.db.database import db
from app.main import app
from app.models.model import TABLES_TO_CREATE


@pytest.fixture(scope="function")
def test_db():
    db.connect(reuse_if_open=True)
    db.create_tables(TABLES_TO_CREATE)
    yield
    db.drop_tables(TABLES_TO_CREATE)
    db.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
