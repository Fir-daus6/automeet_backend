import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Automeet"
    API_VERSION: str = "1.0.0"
    ENV: str = "local"
    FRONTEND_URL: str = "https://v0-auto-meeting-assistant.vercel.app"
    BASE_API_URL: str = "http://localhost:8000"

   
    DB_ENGINE: str = "mysql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307  
    DB_USER: str = "automeet"
    DB_PASSWORD: str = "automeet123"
    DB_NAME: str = "automeet_db"
    DATABASE_URL: str = ""

   
    # JWT / AUTH  
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24   # 24 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7   # 7 days

   
    # REDIS 
   
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str = "default"
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = ""

    # Email (optional - enable later)
    EMAIL_SERVICE: str = "custom"
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_SERVER: str = ""
    MAIL_PORT: int = 587
    MAIL_FROM_NAME: str = "Automeet"

    model_config = ConfigDict(extra="ignore")



# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

settings = Settings()


# DATABASE URL BUILDER
if not settings.DATABASE_URL:
    if settings.DB_ENGINE == "mysql":
        settings.DATABASE_URL = (
            f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
    else:
        raise ValueError("Only MySQL is supported for Automeet.")



# REDIS URL BUILDER
if not settings.REDIS_URL:
    settings.REDIS_URL = (
        f"redis://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}"
        f"@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
    )




