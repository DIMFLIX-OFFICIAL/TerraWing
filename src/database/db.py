from typing import Optional

from .db_settings import SetupDatabase


class Database(SetupDatabase):
    async def drone_exist(self, drone_id: int, secret_key: str) -> bool:
        raise NotImplementedError

    async def get_drone(self, drone_id: int) -> Optional[SetupDatabase]:
        raise NotImplementedError
