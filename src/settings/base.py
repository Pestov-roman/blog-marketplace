from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "local"
    app_env: str = "local"
    debug: bool = True
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24

    pg_host: str = "db"
    pg_port: int = 5432
    pg_db: str = "marketplace_blog"
    pg_user: str = "postgres"
    pg_password: str = "postgres"

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str | None = None
    rabbitmq_password: str | None = None

    s3_endpoint: str = "minio:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "images"
    s3_secure: bool = False

    jwt_secret_key: str = "supersecretkey"
    jwt_exp_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        )

    @property
    def rabbitmq_uri(self) -> str:
        creds = ""
        if self.rabbitmq_user and self.rabbitmq_password:
            creds = f"{self.rabbitmq_user}:{self.rabbitmq_password}@"
        return f"ampq://{creds}{self.rabbitmq_host}:{self.rabbitmq_port}//"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
