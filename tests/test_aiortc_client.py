# client.py
import cv2
import asyncio
import logging
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import websockets
from av.video.frame import VideoFrame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("client")


class CameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # 0 is typically the default camera
        if not self.cap.isOpened():
            logger.error("Unable to open video source")
            raise Exception("Unable to open video source")

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            logger.error("Unable to read from video source")
            raise Exception("Unable to read from video source")

        # Convert the frame to av.VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = None
        video_frame.time_base = None

        return video_frame


async def run_client(uri):
    pc = RTCPeerConnection()

    try:
        pc.addTrack(CameraStreamTrack())
        logger.info("Camera stream track added")

        async with websockets.connect(uri) as ws:
            logger.info(f"Connected to server at {uri}")

            offer = await pc.createOffer()
            await pc.setLocalDescription(offer)

            await ws.send(pc.localDescription.sdp)
            logger.info("Offer sent to server")

            answer = await ws.recv()
            logger.info("Answer received from server")
            await pc.setRemoteDescription(RTCSessionDescription(answer, "answer"))

            # Wait for media to start flowing
            logger.info("Waiting for media to start flowing")
            await asyncio.sleep(30)
    except Exception as e:
        logger.error(e)
    finally:
        await pc.close()
        logger.info("Peer connection closed")

if __name__ == "__main__":
    SERVER_URI = "ws://localhost:8000/ws"
    asyncio.run(run_client(SERVER_URI))
