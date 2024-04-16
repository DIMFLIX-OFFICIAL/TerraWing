import asyncio
import json
import cv2
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer

class FileVideoStreamTrack(VideoStreamTrack):
    def __init__(self, video_source):
        super().__init__()
        self.player = MediaPlayer(video_source)

    async def recv(self):
        frame = await self.player.video.recv()
        return frame

async def connect_to_websocket():
    import websockets
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        pc = RTCPeerConnection()
        video_source = "example.mp4"
        pc.addTrack(FileVideoStreamTrack(video_source))

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        await websocket.send(json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}))

        # Ожидание ответа от сервера
        response = await websocket.recv()
        answer = json.loads(response)
        await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))

        # Обмен ICE кандидатами (необходимо реализовать)

        # Поддерживаем WebSocket открытым
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(connect_to_websocket())