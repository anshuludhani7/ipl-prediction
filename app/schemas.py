from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)


class BetCreate(BaseModel):
    team: str
    weight: int = Field(ge=200, le=2000)


class MatchBase(BaseModel):
    id: int
    team_a: str
    team_b: str
    venue: str | None = None
    prediction_deadline: datetime
    result: str | None

    @field_validator("prediction_deadline", mode="before")
    @classmethod
    def parse_prediction_deadline(cls, v):
        if isinstance(v, str):
            # Expect format like "3/28/2026 18:59:59"
            return datetime.strptime(v, "%m/%d/%Y %H:%M:%S")
        return v

    class Config:
        orm_mode = True

