from uuid import UUID
from .db_settings import SetupDatabase


class Database(SetupDatabase):

    async def drone_exist(self, drone_id: UUID) -> bool:
        return await self.db.fetchval(
            "SELECT EXISTS(SELECT 1 FROM drones WHERE id=$1)",
            drone_id
        )

    async def get_drone(self, drone_id: UUID) -> None:
        return await self.db.fetchrow(
            "SELECT * FROM drones WHERE id=$1",
            drone_id
        )
