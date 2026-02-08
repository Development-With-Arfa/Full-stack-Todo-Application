import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # Better Auth JWT Configuration
    BETTER_AUTH_JWKS_URL: str = "http://localhost:3000/api/auth/jwks"
    BETTER_AUTH_ISSUER: str = "http://localhost:3000"
    BETTER_AUTH_AUDIENCE: str = "http://localhost:3000"

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Debug
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
