from typing import Dict
from aiortc import RTCPeerConnection


class DroneConnections:
    def __init__(self):
        self._connections: Dict[str, RTCPeerConnection] = {}

    def __getitem__(self, drone_id: str) -> RTCPeerConnection:
        return self._connections[drone_id]

    def __setitem__(self, drone_id: str, connection: RTCPeerConnection):
        self._connections[drone_id] = connection

    def __delitem__(self, drone_id: str):
        if drone_id in self._connections:
            self._connections[drone_id].close()
            del self._connections[drone_id]
