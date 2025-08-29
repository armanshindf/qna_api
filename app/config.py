from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):

    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    PROJECT_NAME: str = "Q&A API Service"
    VERSION: str = "1.0.0"  
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10  
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    SECRET_KEY: str = "secret-key"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()