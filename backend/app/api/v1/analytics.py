from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.analytics import get_worm_data, get_partnership_data, get_bowler_analysis

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/matches/{match_id}/worm")
async def worm_chart(
    match_id: str = Path(...),
    innings: int = Query(1, ge=1, le=2),
    db: AsyncSession = Depends(get_db),
):
    data = await get_worm_data(db, match_id, innings)
    return {"match_id": match_id, "innings": innings, "data": data}


@router.get("/matches/{match_id}/batting")
async def batting_analysis(
    match_id: str = Path(...),
    innings: int = Query(1, ge=1, le=2),
    db: AsyncSession = Depends(get_db),
):
    data = await get_partnership_data(db, match_id, innings)
    return {"match_id": match_id, "innings": innings, "data": data}


@router.get("/matches/{match_id}/bowling")
async def bowling_analysis(
    match_id: str = Path(...),
    innings: int = Query(1, ge=1, le=2),
    db: AsyncSession = Depends(get_db),
):
    data = await get_bowler_analysis(db, match_id, innings)
    return {"match_id": match_id, "innings": innings, "data": data}
