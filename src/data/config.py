from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file="../.env", env_file_encoding="utf-8")


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def dsn(self) -> str:
        return f"postgres://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class ServerConfig(BaseSettings, env_prefix="SERVER_"):
    host: str
    port: int


class AppConfig(BaseModel):
    postgres: PostgresConfig
    server: ServerConfig
