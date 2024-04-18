import argparse
import json
import asyncio
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, sdp
from aiortc.contrib.media import MediaPlayer


class FileVideoStreamTrack(VideoStreamTrack):
    def __init__(self, video_source):
        super().__init__()
        self.player = MediaPlayer(video_source)

    async def recv(self):
        frame = await self.player.video.recv()
        return frame


async def connect_to_websocket(url: str, drone_id: str, drone_secret: str, video_source: str) -> None:

    extra_headers = {
        "drone_id": drone_id,
        "drone_secret": drone_secret
    }

    async with websockets.connect(uri=url, extra_headers=extra_headers) as websocket:
        pc = RTCPeerConnection()
        pc.addTrack(FileVideoStreamTrack(video_source))

        @pc.on("icecandidate")
        async def on_icecandidate(event):
            if event.candidate:
                await websocket.send(json.dumps({
                    "candidate": {
                        "candidate": event.candidate.candidate,
                        "sdpMid": event.candidate.sdpMid,
                        "sdpMLineIndex": event.candidate.sdpMLineIndex
                    }
                }))

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        await websocket.send(json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}))

        ##==> Ожидание ответа от сервера
        #################################
        response = await websocket.recv()
        answer = json.loads(response)
        await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))

        ##==> Обработка ICE кандидатов, полученных от сервера
        ######################################################
        async for message in websocket:
            data = json.loads(message)
            candidate_data = data.get("candidate", None)
            if "candidate" in data and candidate_data is not None:
                candidate = sdp.candidate_from_sdp(data["candidate"])
                candidate.sdpMid = candidate_data["sdpMid"]
                candidate.sdpMLineIndex = candidate_data["sdpMLineIndex"]
                await pc.addIceCandidate(candidate)

        await asyncio.sleep(1)  # Поддерживаем WebSocket открытым


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Test Video Stream Client',
        description='The program tests communication with the server via aiortc by transmitting a video stream.'
    )
    parser.add_argument('drone_id')
    parser.add_argument('drone_secret')
    args = parser.parse_args()

    if args.drone_id is None:
        raise Exception('--drone_id must be specified')

    if args.drone_secret is None:
        raise Exception('--drone_secret must be specified')

    asyncio.run(connect_to_websocket(
        url="ws://localhost:5000/ws",
        drone_id=args.drone_id,
        drone_secret=args.drone_secret,
        video_source="example.mp4"
    ))
