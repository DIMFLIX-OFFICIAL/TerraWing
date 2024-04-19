import json
import asyncio
import argparse
import platform
import websockets
from typing import Optional, Any, Union
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, sdp
from aiortc.contrib.media import MediaPlayer
from av import Packet
from av.frame import Frame


class FileVideoStreamTrack(VideoStreamTrack):
    def __init__(self, video_source):
        super().__init__()
        self.player = video_source

    async def recv(self) -> Union[Frame, Packet]:
        frame = await self.player.video.recv()
        return frame


def create_media_player(video_source: Optional[str]) -> MediaPlayer:
    if video_source is None:
        webcam = MediaPlayer("/dev/video0", format="v412")

        if platform.system() == "Darwin":
            webcam = MediaPlayer("default:none", format="avfoundation")
        elif platform.system() == "Windows":
            webcam = MediaPlayer("video=Integrated Camera", format="dshow")

        return webcam
    else:
        return MediaPlayer(video_source)


async def connect_to_websocket(url: str, drone_id: str, drone_secret: str, video_source: str = None) -> None:
    extra_headers = {
        "drone_id": drone_id,
        "drone_secret": drone_secret
    }

    async with websockets.connect(uri=url, extra_headers=extra_headers) as websocket:
        pc = RTCPeerConnection()
        player = create_media_player(video_source)
        pc.addTrack(FileVideoStreamTrack(player))

        @pc.on("icecandidate")
        async def on_icecandidate(event: Any) -> None:
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

        response = await websocket.recv()
        answer = json.loads(response)
        await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))

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
    parser.add_argument(
        '--video_source',
        default=None,
        help="Path to the video file or 'webcam' for live webcam feed. If not specified, webcam is used by default."
    )

    args = parser.parse_args()
    asyncio.run(connect_to_websocket(
        url="ws://localhost:5000/ws",
        drone_id=args.drone_id,
        drone_secret=args.drone_secret,
        video_source=args.video_source
    ))
