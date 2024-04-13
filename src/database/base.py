from asyncpg import Pool, create_pool
from abc import ABC, abstractmethod
from loguru import logger


class BaseDB(ABC):
    db: Pool

    @abstractmethod
    async def _create_tables(self) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def _create_connection(dsn: str) -> Pool:
        raise NotImplementedError

    async def close(self):
        """
        Закрытие соединения базы данных
        :return:
        """
        await self.db.close()
        logger.success('Database closed')

    async def setup(self, dsn: str):
        self.db = await self._create_connection(dsn)
        await self._create_tables()
        logger.success("The database was initialized successfully")

