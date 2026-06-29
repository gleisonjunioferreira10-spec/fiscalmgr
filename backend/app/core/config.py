from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gerente Fiscal"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/gerente_fiscal"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 12

    class Config:
        env_file = ".env"

    @field_validator("DATABASE_URL")
    @classmethod
    def _normalizar_driver_postgres(cls, valor: str) -> str:
        if valor.startswith("postgres://"):
            return valor.replace("postgres://", "postgresql+psycopg2://", 1)
        if valor.startswith("postgresql://"):
            return valor.replace("postgresql://", "postgresql+psycopg2://", 1)
        return valor


settings = Settings()
