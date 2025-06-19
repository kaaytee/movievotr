from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import db, init_db
from app.api.api import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    print("Connecting to the database...")
    if db.is_closed():
        db.connect()
    init_db()


    yield
    # on shutdown
    print("Closing database connection...")
    if not db.is_closed():
        db.close()


app = FastAPI(lifespan=lifespan, title="MovieVotr API")

app.include_router(api_router, prefix=settings.API_URL)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MovieVotr API!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}