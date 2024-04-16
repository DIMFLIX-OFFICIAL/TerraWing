from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
import threading

app = FastAPI()

pc = RTCPeerConnection()
display_track = None


class VideoDisplayTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()  # don't forget to initialize base class
        self.frames = []

    async def recv(self):
        frame = await super().recv()
        self.frames.append(frame)
        return frame


def display_frames(track):
    while True:
        if track.frames:
            frame = track.frames.pop(0)
            if frame is not None:
                img = frame.to_ndarray(format="bgr24")
                cv2.imshow("Video", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


@app.on_event("startup")
async def startup():
    global display_track
    display_track = VideoDisplayTrack()
    pc.addTrack(display_track)

    # Start display in a separate thread
    threading.Thread(target=display_frames, args=(display_track,), daemon=True).start()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    @pc.on("track")
    async def on_track(track):
        print("Track received:", track)

    try:
        while True:
            offer = await websocket.receive_text()
            await pc.setRemoteDescription(RTCSessionDescription(offer, "offer"))

            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)
            await websocket.send_text(pc.localDescription.sdp)

    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/")
async def get():
    return "WebRTC Video Receiver Server"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
