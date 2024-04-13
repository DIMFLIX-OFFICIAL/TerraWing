from fastapi import FastAPI

from data.logger_config import setup_logging
from data.config import AppConfig, PostgresConfig, ServerConfig
from database.db import Database


setup_logging()  # Устанавливаем логирование с помощью Loguru

cfg: AppConfig = AppConfig(
    postgres=PostgresConfig(),
    server=ServerConfig()
)
db = Database()
app = FastAPI()
