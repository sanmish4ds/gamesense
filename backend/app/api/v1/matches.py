from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import get_redis
from app.models.match import Match
from app.schemas.match import MatchListResponse, MatchDetailResponse
from app.services.scorecard import build_live_scorecard
import json

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchListResponse])
async def list_matches(
    live_only: bool = Query(False),
    match_type: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Match).order_by(desc(Match.updated_at)).limit(50)
    if live_only:
        stmt = stmt.where(Match.is_live == True)
    if match_type:
        stmt = stmt.where(Match.match_type == match_type.upper())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/live", response_model=list[MatchListResponse])
async def list_live_matches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Match).where(Match.is_live == True).order_by(desc(Match.updated_at))
    )
    return result.scalars().all()


@router.get("/{match_id}", response_model=MatchDetailResponse)
async def get_match(match_id: str, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    # Try Redis cache first
    cached = await redis.get(f"live:{match_id}")
    if cached:
        data = json.loads(cached)
        result = await db.execute(select(Match).where(Match.id == match_id))
        match = result.scalar_one_or_none()
        if match:
            return match

    result = await db.execute(select(Match).where(Match.id == match_id))
    match = result.scalar_one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/{match_id}/scorecard")
async def get_scorecard(match_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Match).where(Match.id == match_id))
    match = result.scalar_one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return build_live_scorecard(match)
