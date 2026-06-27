from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.player import Player
from app.schemas.player import PlayerResponse
from app.services.cricapi import cricapi

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/search", response_model=list[PlayerResponse])
async def search_players(q: str = Query(..., min_length=2), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Player).where(Player.name.ilike(f"%{q}%")).limit(20)
    )
    players = result.scalars().all()
    if not players:
        # Fall back to live API search
        api_results = await cricapi.search_player(q)
        return [
            PlayerResponse(
                id=p.get("id", ""),
                name=p.get("name", ""),
                country=p.get("country"),
            )
            for p in api_results[:10]
        ]
    return players


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Player).where(Player.id == player_id))
    player = result.scalar_one_or_none()
    if player:
        return player

    # Fetch from API and cache
    try:
        data = await cricapi.get_player_info(player_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Player not found")

    player = Player(
        id=player_id,
        name=data.get("name", ""),
        full_name=data.get("fullName"),
        country=data.get("country"),
        date_of_birth=data.get("dateOfBirth"),
        role=data.get("role"),
        batting_style=data.get("battingStyle"),
        bowling_style=data.get("bowlingStyle"),
        image_url=data.get("playerImg"),
    )
    db.add(player)
    await db.commit()
    await db.refresh(player)
    return player
