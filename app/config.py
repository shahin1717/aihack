try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    # -------------------------
    # DATABASE CONFIG (AlwaysData MySQL)
    # Example .env format:
    # DATABASE_URL="mysql+pymysql://user:password@mysql-yourname.alwaysdata.net/dbname"
    # -------------------------
    DATABASE_URL: str = "mysql+pymysql://user:password@host/dbname"

    # -------------------------
    # SECURITY (JWT)
    # -------------------------
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # -------------------------
    # SMTP EMAIL SETTINGS
    # -------------------------
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""


    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
