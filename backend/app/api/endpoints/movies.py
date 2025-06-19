from typing import Any, List
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("/tmdb/search", response_model=List[Any])
async def search_tmdb_movies(
    query: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Proxies a search request to the TMDb API.
    """
    if not query:
        return []
    
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": query,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.TMDB_API_URL}/search/movie", params=params)
            response.raise_for_status()
            return response.json().get("results", [])
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching from TMDb API")
        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="TMDb API is unavailable")


@router.post("/catalog", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED)
def add_movie_to_catalog(
    movie_in: schemas.MovieCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Adds a movie to the internal catalog if it doesn't already exist.
    Returns the internal movie record.
    """
    # Check if movie with the same tmdb_id already exists
    db_movie = crud.crud_movie.get_movie_by_tmdb_id(tmdb_id=movie_in.tmdb_id)
    if db_movie:
        # If it exists, we can just return it.
        # Or, you could raise an error if you want to be strict.
        return db_movie
    
    # If not, create it
    return crud.crud_movie.create_movie(movie_in=movie_in) 