from uuid import UUID
from loguru import logger
from dataclasses import dataclass
from typing import Dict, Optional
from aiortc import RTCPeerConnection

from neural_network import VideoTransformTrack


@dataclass
class DroneConnect:
    pc: RTCPeerConnection
    track: Optional[VideoTransformTrack]


class DroneConnections:
    def __init__(self) -> None:
        self._connections: Dict[UUID, DroneConnect] = {}

    def __getitem__(self, drone_id: UUID) -> DroneConnect:
        return self._connections[drone_id]

    def __setitem__(self, drone_id: UUID, connection: DroneConnect) -> None:
        self._connections[drone_id] = connection
        logger.debug(f"Drone {drone_id} added to connections list")

    async def delete(self, drone_id: UUID) -> None:
        if drone_id in self._connections:
            self._connections[drone_id].track.close()
            await self._connections[drone_id].pc.close()
            del self._connections[drone_id]
            logger.debug(f"The connection with {drone_id} has been completed correctly!")
