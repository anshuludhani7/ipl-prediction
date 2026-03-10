from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)


class BetCreate(BaseModel):
    team: str
    weight: int = Field(ge=200, le=2000)


class MatchBase(BaseModel):
    id: int
    team_a: str
    team_b: str
    start_time: datetime
    prediction_deadline: datetime
    result: str | None

    class Config:
        orm_mode = True

