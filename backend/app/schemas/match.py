from datetime import datetime
from typing import Any
from pydantic import BaseModel, model_validator


class ScoreEntry(BaseModel):
    runs: int = 0
    wickets: int = 0
    overs: float = 0.0
    run_rate: float = 0.0
    inning: str = ""

    @model_validator(mode="before")
    @classmethod
    def normalise_cricapi_keys(cls, data: Any) -> Any:
        """CricAPI returns r/w/o shorthand; normalise to full names."""
        if isinstance(data, dict):
            overs_raw = data.get("o") or data.get("overs") or 0
            try:
                overs = float(overs_raw)
            except (TypeError, ValueError):
                overs = 0.0
            runs = int(data.get("r") or data.get("runs") or 0)
            rr = round(runs / overs, 2) if overs > 0 else 0.0
            return {
                "runs": runs,
                "wickets": int(data.get("w") or data.get("wickets") or 0),
                "overs": overs,
                "run_rate": data.get("run_rate", rr),
                "inning": data.get("inning", ""),
            }
        return data


class MatchBase(BaseModel):
    id: str
    name: str
    match_type: str | None = None
    status: str | None = None
    venue: str | None = None
    date: str | None = None
    date_time_gmt: str | None = None
    team1_name: str | None = None
    team2_name: str | None = None
    is_live: bool = False
    score: list[ScoreEntry] | None = None
    batting_team: str | None = None
    bowling_team: str | None = None
    current_over: float | None = None
    match_winner: str | None = None


class MatchListResponse(MatchBase):
    model_config = {"from_attributes": True}


class MatchDetailResponse(MatchBase):
    scorecard: dict | None = None
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}
