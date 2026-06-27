"""
WebSocket endpoint — subscribes to Redis pub/sub channel for a match
and pushes score updates to all connected browser clients.
"""

import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as aioredis

from app.core.config import settings

router = APIRouter()

# match_id -> set of WebSockets
_connections: dict[str, set[WebSocket]] = {}


@router.websocket("/ws/matches/{match_id}")
async def match_websocket(websocket: WebSocket, match_id: str):
    await websocket.accept()

    if match_id not in _connections:
        _connections[match_id] = set()
    _connections[match_id].add(websocket)

    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"match:{match_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"]
                # Fan-out to all connected clients for this match
                dead = set()
                for ws in _connections.get(match_id, set()):
                    try:
                        await ws.send_text(data)
                    except Exception:
                        dead.add(ws)
                _connections[match_id] -= dead
    except WebSocketDisconnect:
        pass
    finally:
        _connections.get(match_id, set()).discard(websocket)
        await pubsub.unsubscribe(f"match:{match_id}")
        await redis.aclose()
