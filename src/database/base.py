from asyncpg import Pool
from loguru import logger
from abc import ABC, abstractmethod


class BaseDB(ABC):
    db: Pool
    __slots__ = ("db",)

    @staticmethod
    @abstractmethod
    async def _create_connection(dsn: str) -> Pool:
        raise NotImplementedError

    @abstractmethod
    async def _create_extensions(self) -> None:
        """ Подключение плагинов """
        raise NotImplementedError

    @abstractmethod
    async def _create_triggers(self) -> None:
        """ Создание триггеров """
        raise NotImplementedError

    @abstractmethod
    async def _create_tables(self) -> None:
        """ Создание таблиц """
        raise NotImplementedError

    async def close(self) -> None:
        """ Закрытие соединения базы данных """
        await self.db.close()
        logger.success('Database closed')

    async def setup(self, dsn: str) -> None:
        """ Метод с полной настройкой базы данных """
        self.db = await self._create_connection(dsn)
        await self._create_extensions()
        await self._create_tables()
        logger.success("The database was initialized successfully")
