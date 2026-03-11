from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Enum,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    bankroll: Mapped[int] = mapped_column(Integer, default=20000)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    bets: Mapped[list["Bet"]] = relationship("Bet", back_populates="user")


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_a: Mapped[str] = mapped_column(String(64))
    team_b: Mapped[str] = mapped_column(String(64))
    venue: Mapped[str | None] = mapped_column(String(128), nullable=True)
    prediction_deadline: Mapped[datetime] = mapped_column(DateTime, index=True)
    # result: "A", "B", or None for not yet decided
    result: Mapped[str | None] = mapped_column(
        String(1), nullable=True
    )

    bets: Mapped[list["Bet"]] = relationship("Bet", back_populates="match")


class Bet(Base):
    __tablename__ = "bets"
    __table_args__ = (
        UniqueConstraint("user_id", "match_id", name="unique_user_match_bet"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), index=True)
    # "A" or "B"
    team: Mapped[str] = mapped_column(String(1))
    weight: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Payout amount once the match is settled (can be computed later).
    payout_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    settled: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", back_populates="bets")
    match: Mapped["Match"] = relationship("Match", back_populates="bets")

