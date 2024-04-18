from typing import Union
from uuid import UUID
from aiortc import MediaStreamTrack
from loguru import logger
from av.frame import Frame
from av.packet import Packet
import cv2
import asyncio
import concurrent.futures

class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, drone_id: UUID, track: MediaStreamTrack) -> None:
        super().__init__()
        self.drone_id: UUID = drone_id
        self.track: MediaStreamTrack = track
        self._frame = None
        self._window_name = f"Drone {self.drone_id}"
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._loop = asyncio.get_event_loop()
        self._loop.run_in_executor(self._executor, self.display_video)

    async def recv(self) -> Union[Frame, Packet]:
        frame: Union[Frame, Packet] = await self.track.recv()
        # Конвертируем frame в массив numpy для OpenCV
        self._frame = frame.to_ndarray(format='bgr24')
        logger.debug(f"Получен кадр от дрона {self.drone_id}")
        return frame

    def display_video(self):
        cv2.namedWindow(self._window_name, cv2.WINDOW_NORMAL)
        while True:
            if self._frame is not None:
                cv2.imshow(self._window_name, self._frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()

    def __del__(self):
        # Убедимся, что окно закрыто и исполнитель остановлен
        cv2.destroyWindow(self._window_name)
        self._executor.shutdown()
