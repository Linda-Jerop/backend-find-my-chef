import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Find My Chef API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "sqlite:///./find_my_chef.db"  # Use PostgreSQL in production: postgresql://user:password@host/dbname
    
    SECRET_KEY: str = "your-secret-key-here"  # TODO: Generate with python -c 'import secrets; print(secrets.token_urlsafe(32))'
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # Tokens expire after 24 hours.
    
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]  # Add your production frontend URL here.
    
    FIREBASE_CREDENTIALS_PATH: str = ""  # TODO: Add path to your Firebase service account JSON file.
    FIREBASE_PROJECT_ID: str = ""  # TODO: Add your Firebase project ID.
    
    ITEMS_PER_PAGE: int = 20
    MAX_ITEMS_PER_PAGE: int = 100
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
