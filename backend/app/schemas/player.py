from pydantic import BaseModel


class PlayerBase(BaseModel):
    id: str
    name: str
    full_name: str | None = None
    country: str | None = None
    role: str | None = None
    batting_style: str | None = None
    bowling_style: str | None = None
    image_url: str | None = None
    batting_avg: float | None = None
    bowling_avg: float | None = None
    batting_sr: float | None = None
    economy: float | None = None
    matches: int = 0
    runs: int = 0
    wickets: int = 0

    model_config = {"from_attributes": True}


class PlayerResponse(PlayerBase):
    pass
