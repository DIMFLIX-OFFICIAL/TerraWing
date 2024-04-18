import cv2
import asyncio
import numpy as np
from uuid import UUID
from loguru import logger
from typing import Union, Final
import concurrent.futures
from av.frame import Frame
from ultralytics import YOLO
from av.packet import Packet
from aiortc import MediaStreamTrack
from av.video.frame import VideoFrame

model: Final[YOLO] = YOLO('data/weights/best.pt')


class VideoTransformTrack(MediaStreamTrack):
    SHOW_VIDEO = True
    kind = "video"

    def __init__(self, drone_id: UUID, track: MediaStreamTrack) -> None:
        super().__init__()
        self.drone_id: UUID = drone_id
        self.track: MediaStreamTrack = track
        self._frame = None

        if self.SHOW_VIDEO:
            self._show_video_running = True
            self._window_name = f"Drone {self.drone_id}"
            self._loop = asyncio.get_event_loop()
            self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            self._loop.run_in_executor(self._executor, self.display_video)

    @staticmethod
    def process_frame(frame: np.ndarray) -> np.ndarray:
        img = cv2.resize(frame, (1280, 720))  # Измененное изображение
        results = model.predict(img, imgsz=1280)

        for r in results:
            classes = r.boxes.cls.cpu().numpy()  # Классы
            name_classes = r.names  # Словарь классов
            boxes = r.boxes.xyxy.cpu().numpy().astype(int)  # Координаты объектов и конвертация в int

            # Векторизованное рисование прямоугольников и текста
            for box, cls in zip(boxes, classes):
                xmin, ymin, xmax, ymax = box
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 255), 2)
                cv2.putText(img, name_classes[cls], (xmin, ymin),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

        return img  # Возвращаем измененное изображение с нарисованными прямоугольниками и текстом

    async def recv(self) -> Union[Frame, Packet]:
        frame: Union[Frame, Packet, VideoFrame] = await self.track.recv()
        self._frame = frame.to_ndarray(format='bgr24')
        return frame

    def display_video(self) -> None:
        cv2.namedWindow(self._window_name, cv2.WINDOW_NORMAL)

        while self._show_video_running:
            if self._frame is not None:
                #frame = self._frame
                frame = self.process_frame(self._frame)  # Обрабатываем нейронкой
                cv2.imshow(self._window_name, frame)  # показыаваем
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()

    def close(self) -> None:
        if self.SHOW_VIDEO:
            self._show_video_running = False
            if self._executor:
                self._executor.shutdown(wait=True)
