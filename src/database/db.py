from typing import Optional
from uuid import UUID
from .db_settings import SetupDatabase, DictRecord


class Database(SetupDatabase):
    """ API для взаимодействия с базой данных """
    async def drone_exist(self, drone_id: UUID) -> bool:
        """ Проверяем дрона по id на наличие в базе данных """
        return await self.db.fetchval(
            "SELECT EXISTS(SELECT 1 FROM drones WHERE id=$1)",
            drone_id
        )

    async def get_drone(self, drone_id: UUID) -> Optional[DictRecord]:
        """ Получаем все данные о дроне """
        return await self.db.fetchrow(
            "SELECT * FROM drones WHERE id=$1",
            drone_id
        )
