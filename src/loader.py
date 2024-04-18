from typing import Final
from fastapi import FastAPI

from database.db import Database
from data.logger_config import setup_logging
from data.drone_connections import DroneConnections
from data.config import AppConfig, PostgresConfig, ServerConfig


setup_logging()  # Устанавливаем логирование с помощью Loguru

cfg: Final[AppConfig] = AppConfig(
    postgres=PostgresConfig(),
    server=ServerConfig()
)

db: Final[Database] = Database()
app: Final[FastAPI] = FastAPI()
drones: Final[DroneConnections] = DroneConnections()
