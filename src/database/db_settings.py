from typing import Any
from asyncpg import Record, Pool, create_pool

from .base import BaseDB


class DictRecord(Record):
    """ Класс для представления Row от asyncpg в виде словаря """
    __slots__ = ()

    def __getitem__(self, key) -> Any:
        value = super().__getitem__(key)
        if isinstance(value, Record):
            return dict(value.items())
        return value

    def to_dict(self) -> dict:
        return dict(super().items())

    def __repr__(self) -> str:
        return str(dict(super().items()))


class SetupDatabase(BaseDB):
    @staticmethod
    async def _create_connection(dsn: str) -> Pool:
        return await create_pool(
            dsn=dsn,
            record_class=DictRecord
        )

    async def _create_extensions(self) -> None:
        await self.db.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    async def _create_triggers(self) -> None: ...

    async def _create_tables(self) -> None:
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS drones(
                id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
                secret_key TEXT NOT NULL
        )""")
