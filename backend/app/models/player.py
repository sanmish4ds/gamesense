from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=True)  # batsman/bowler/allrounder/keeper
    batting_style: Mapped[str] = mapped_column(String(50), nullable=True)
    bowling_style: Mapped[str] = mapped_column(String(50), nullable=True)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=True)
    date_of_birth: Mapped[str] = mapped_column(String(20), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Career stats
    batting_avg: Mapped[float] = mapped_column(Float, nullable=True)
    bowling_avg: Mapped[float] = mapped_column(Float, nullable=True)
    batting_sr: Mapped[float] = mapped_column(Float, nullable=True)
    economy: Mapped[float] = mapped_column(Float, nullable=True)
    matches: Mapped[int] = mapped_column(Integer, default=0)
    runs: Mapped[int] = mapped_column(Integer, default=0)
    wickets: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    team: Mapped["Team"] = relationship("Team", back_populates="players")
