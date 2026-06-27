from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ball_event import BallEvent


async def get_worm_data(db: AsyncSession, match_id: str, innings: int) -> list[dict]:
    """Cumulative runs per over for worm chart."""
    result = await db.execute(
        select(
            BallEvent.over,
            func.sum(BallEvent.runs + BallEvent.extras).label("over_runs"),
        )
        .where(BallEvent.match_id == match_id, BallEvent.innings == innings)
        .group_by(BallEvent.over)
        .order_by(BallEvent.over)
    )
    rows = result.all()
    cumulative = 0
    worm = []
    for row in rows:
        cumulative += row.over_runs
        worm.append({"over": row.over + 1, "cumulative_runs": cumulative, "over_runs": row.over_runs})
    return worm


async def get_partnership_data(db: AsyncSession, match_id: str, innings: int) -> list[dict]:
    """Runs per batsman partnership (runs grouped by batsman)."""
    result = await db.execute(
        select(
            BallEvent.batsman,
            func.sum(BallEvent.runs).label("runs"),
            func.count(BallEvent.id).label("balls"),
            func.sum(BallEvent.is_boundary.cast(int)).label("fours"),
            func.sum(BallEvent.is_six.cast(int)).label("sixes"),
        )
        .where(BallEvent.match_id == match_id, BallEvent.innings == innings)
        .group_by(BallEvent.batsman)
        .order_by(func.sum(BallEvent.runs).desc())
    )
    return [
        {
            "batsman": row.batsman,
            "runs": row.runs,
            "balls": row.balls,
            "fours": row.fours,
            "sixes": row.sixes,
            "strike_rate": round((row.runs / row.balls) * 100, 2) if row.balls else 0,
        }
        for row in result.all()
    ]


async def get_bowler_analysis(db: AsyncSession, match_id: str, innings: int) -> list[dict]:
    result = await db.execute(
        select(
            BallEvent.bowler,
            func.count(BallEvent.id).label("balls"),
            func.sum(BallEvent.runs + BallEvent.extras).label("runs"),
            func.sum(BallEvent.is_wicket.cast(int)).label("wickets"),
        )
        .where(BallEvent.match_id == match_id, BallEvent.innings == innings)
        .group_by(BallEvent.bowler)
        .order_by(func.sum(BallEvent.is_wicket.cast(int)).desc())
    )
    return [
        {
            "bowler": row.bowler,
            "overs": round(row.balls / 6, 1),
            "runs": row.runs,
            "wickets": row.wickets,
            "economy": round((row.runs / (row.balls / 6)), 2) if row.balls else 0,
        }
        for row in result.all()
    ]
