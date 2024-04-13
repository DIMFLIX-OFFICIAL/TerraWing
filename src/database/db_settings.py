from asyncpg import Record, Pool, create_pool

from .base import BaseDB


class DictRecord(Record):
    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, Record):
            return dict(value.items())
        return value

    def to_dict(self):
        return dict(super().items())

    def __repr__(self):
        return str(dict(super().items()))


class SetupDatabase(BaseDB):
    @staticmethod
    async def _create_connection(dsn: str) -> Pool:
        return await create_pool(
            dsn=dsn,
            record_class=DictRecord
        )

    async def _create_tables(self):
        ...
