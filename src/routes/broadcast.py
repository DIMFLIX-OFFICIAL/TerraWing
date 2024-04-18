from uuid import UUID
from loguru import logger
from pydantic import BaseModel
from fastapi.routing import APIRouter
from fastapi import WebSocket, HTTPException, WebSocketDisconnect
from aiortc import RTCPeerConnection, RTCSessionDescription, sdp
from aiortc.contrib.media import MediaRelay

from loader import db, drones
from neural_network.ai import VideoTransformTrack


class WebSocketQuery(BaseModel):
    id: UUID
    secret_key: str


router = APIRouter()
relay = MediaRelay()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):

    ##==> Валидация входных авторизационных данных
    ###############################################
    drone_id = ws.headers.get('drone_id')
    drone_secret = ws.headers.get('drone_secret')
    if drone_id is None or drone_secret is None:
        await ws.close(code=1008)
        raise HTTPException(status_code=403, detail="Missing headers")

    try:
        drone_id = UUID(drone_id)
    except ValueError:
        await ws.close(code=4000)
        raise HTTPException(status_code=403, detail="Invalid type 'drone_id'")

    if not isinstance(drone_secret, str):
        raise HTTPException(status_code=403, detail="Invalid type 'drone_secret'")

    drone = await db.get_drone(drone_id)
    if drone is None or drone["secret_key"] != drone_secret:
        await ws.close(code=1008)
        raise HTTPException(status_code=403, detail="Invalid authorization data")

    ##==> Логика подключения aiortc
    ################################
    await ws.accept()
    pc = RTCPeerConnection()
    drones[drone_id] = pc

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.debug(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "failed":
            await pc.close()
            del drones[drone_id]

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            local_video = VideoTransformTrack(
                drone_id=drone_id,
                track=relay.subscribe(track)
            )
            pc.addTrack(local_video)

    @pc.on("icecandidate")
    async def on_icecandidate(event):
        logger.debug("on_icecandidate: ", event)
        if event.candidate:
            await ws.send_json({
                "candidate": {
                    "candidate": event.candidate.candidate,
                    "sdpMid": event.candidate.sdpMid,
                    "sdpMLineIndex": event.candidate.sdpMLineIndex
                }
            })

    try:
        while True:
            data = await ws.receive_json()
            candidate_data = data.get("candidate", None)
            sdp_data = data.get("sdp", None)
            type_data = data.get("type", None)

            if sdp_data is not None and type_data is not None:
                offer = RTCSessionDescription(sdp=sdp_data, type=type_data)
                await pc.setRemoteDescription(offer)
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await ws.send_json({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})
            elif candidate_data is not None:
                candidate = sdp.candidate_from_sdp(data["candidate"])
                candidate.sdpMid = candidate_data["sdpMid"]
                candidate.sdpMLineIndex = candidate_data["sdpMLineIndex"]
                await pc.addIceCandidate(candidate)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
        await pc.close()
        del drones[drone_id]
