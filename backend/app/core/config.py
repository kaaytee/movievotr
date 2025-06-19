from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
dotenv_path = os.path.join(backend_dir, '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # TMDB API
    TMDB_API_KEY: str
    TMDB_API_URL: str = "https://api.themoviedb.org/3"

    # BACKEND API
    API_URL: str = os.getenv("API_URL", "/api/v1")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")


    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings() 