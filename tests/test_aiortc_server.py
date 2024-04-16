from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaRelay

app = FastAPI()
relay = MediaRelay()


class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        print(frame)
        # Трансформации с видео можно проводить здесь
        return frame


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("track")
    def on_track(track):
        print("Track received")
        print(track.kind)
        if track.kind == "video":
            local_video = VideoTransformTrack(relay.subscribe(track))
            pc.addTrack(local_video)

    try:
        while True:
            data = await websocket.receive_json()
            if "sdp" in data:
                offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                await pc.setRemoteDescription(offer)
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await websocket.send_json({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})
            elif "candidate" in data:
                pass  # Обработка ICE кандидатов
    except WebSocketDisconnect:
        print("Client disconnected")
        await pc.close()
        pcs.discard(pc)

pcs = set()  # keep track of peer connections

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
