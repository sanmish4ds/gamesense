from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, Integer, JSON, func, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    match_type: Mapped[str] = mapped_column(String(20), nullable=True)  # T20/ODI/Test
    status: Mapped[str] = mapped_column(Text, nullable=True)
    venue: Mapped[str] = mapped_column(String(200), nullable=True)
    date: Mapped[str] = mapped_column(String(30), nullable=True)
    date_time_gmt: Mapped[str] = mapped_column(String(50), nullable=True)

    team1_id: Mapped[str] = mapped_column(String, nullable=True)
    team1_name: Mapped[str] = mapped_column(String(100), nullable=True)
    team2_id: Mapped[str] = mapped_column(String, nullable=True)
    team2_name: Mapped[str] = mapped_column(String(100), nullable=True)

    # Live state (updated each poll)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[dict] = mapped_column(JSON, nullable=True)        # raw score array from API
    toss: Mapped[dict] = mapped_column(JSON, nullable=True)
    current_over: Mapped[float] = mapped_column(Float, nullable=True)
    batting_team: Mapped[str] = mapped_column(String(100), nullable=True)
    bowling_team: Mapped[str] = mapped_column(String(100), nullable=True)
    match_winner: Mapped[str] = mapped_column(String(200), nullable=True)

    # Full scorecard from API (cached)
    scorecard: Mapped[dict] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    ball_events: Mapped[list["BallEvent"]] = relationship("BallEvent", back_populates="match")
