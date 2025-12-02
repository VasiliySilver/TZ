from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent.parent.parent


class DatabaseConfig(BaseSettings):
    """Database configuration"""
    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")
    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    database: str = Field(..., alias="POSTGRES_DB")

    @property
    def url(self) -> str:
        """Get database URL for SQLAlchemy"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = SettingsConfigDict(
        env_file=(env_path / '.env', env_path / '.env.local'),
        extra='ignore'
    )


db_config = DatabaseConfig()