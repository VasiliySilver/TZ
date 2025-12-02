from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent.parent.parent


class RabbitMQConfig(BaseSettings):
    """RabbitMQ configuration"""
    host: str = Field(..., alias="RABBITMQ_HOST")
    port: int = Field(..., alias="RABBITMQ_PORT")
    user: str = Field(..., alias="RABBITMQ_USER")
    password: str = Field(..., alias="RABBITMQ_PASSWORD")

    @property
    def url(self) -> str:
        """Get RabbitMQ connection URL"""
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"

    model_config = SettingsConfigDict(
        env_file=(env_path / '.env', env_path / '.env.local'),
        extra='ignore'
    )


rabbitmq_config = RabbitMQConfig()