from typing import Union
from uuid import UUID
from aiortc import MediaStreamTrack
from loguru import logger
from av.frame import Frame
from av.packet import Packet


class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, drone_id: UUID, track: MediaStreamTrack) -> None:
        super().__init__()
        self.drone_id: UUID = drone_id
        self.track: MediaStreamTrack = track

    async def recv(self) -> Union[Frame, Packet]:
        frame: Union[Frame, Packet] = await self.track.recv()
        # frame.to_ndarray(format='bgr24')
        logger.debug(f"Получен кадр от дрона {self.drone_id}")
        return frame
