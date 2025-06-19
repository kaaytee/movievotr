from fastapi import APIRouter

from .endpoints import users, groups, movies, polls, admin

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(polls.router, prefix="/polls", tags=["polls"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

