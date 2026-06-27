from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Boolean, Float, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class BallEvent(Base):
    __tablename__ = "ball_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[str] = mapped_column(String, ForeignKey("matches.id"), nullable=False)

    # Over/ball position
    over: Mapped[int] = mapped_column(Integer, nullable=False)
    ball: Mapped[int] = mapped_column(Integer, nullable=False)
    innings: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Delivery details
    batsman: Mapped[str] = mapped_column(String(100), nullable=True)
    bowler: Mapped[str] = mapped_column(String(100), nullable=True)
    runs: Mapped[int] = mapped_column(Integer, default=0)
    extras: Mapped[int] = mapped_column(Integer, default=0)
    extra_type: Mapped[str] = mapped_column(String(20), nullable=True)  # wide/noball/bye/legbye

    # Outcomes
    is_wicket: Mapped[bool] = mapped_column(Boolean, default=False)
    wicket_type: Mapped[str] = mapped_column(String(50), nullable=True)
    wicket_player: Mapped[str] = mapped_column(String(100), nullable=True)
    is_boundary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_six: Mapped[bool] = mapped_column(Boolean, default=False)

    # Cumulative state at this delivery
    total_runs: Mapped[int] = mapped_column(Integer, default=0)
    total_wickets: Mapped[int] = mapped_column(Integer, default=0)
    run_rate: Mapped[float] = mapped_column(Float, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    match: Mapped["Match"] = relationship("Match", back_populates="ball_events")

    __table_args__ = (
        Index("ix_ball_events_match_innings", "match_id", "innings", "over", "ball"),
    )
