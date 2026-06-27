from fastapi import APIRouter
from app.api.v1 import matches, players, analytics

router = APIRouter(prefix="/api/v1")
router.include_router(matches.router)
router.include_router(players.router)
router.include_router(analytics.router)
