import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_router
from app.api.websocket import router as ws_router
from app.core.config import settings
from app.core.redis_client import close_redis
from app.workers.poller import poll


async def _polling_loop():
    while True:
        try:
            await poll()
        except Exception as exc:
            print(f"[Poller] Error: {exc}")
        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_polling_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await close_redis()


app = FastAPI(
    title="GameSense Cricket Analytics",
    description="Real-time T20 cricket analytics platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "gamesense-backend"}
