from datetime import datetime
from pydantic import BaseModel


class BallEventSchema(BaseModel):
    id: int
    match_id: str
    over: int
    ball: int
    innings: int
    batsman: str | None = None
    bowler: str | None = None
    runs: int = 0
    extras: int = 0
    extra_type: str | None = None
    is_wicket: bool = False
    wicket_type: str | None = None
    wicket_player: str | None = None
    is_boundary: bool = False
    is_six: bool = False
    total_runs: int = 0
    total_wickets: int = 0
    run_rate: float | None = None
    timestamp: datetime

    model_config = {"from_attributes": True}


class LiveMatchEvent(BaseModel):
    """Pushed over WebSocket to connected clients."""
    type: str = "score_update"
    match_id: str
    score: list | None = None
    status: str | None = None
    batting_team: str | None = None
    bowling_team: str | None = None
    current_over: float | None = None
    scorecard: dict | None = None
    latest_ball: BallEventSchema | None = None
