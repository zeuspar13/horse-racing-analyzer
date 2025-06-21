from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class RaceBase(BaseModel):
    race_date: datetime
    track: str
    distance: int = Field(..., ge=0)
    race_type: str
    class_rating: Optional[int] = None
    total_runners: Optional[int] = None


class RaceCreate(RaceBase):
    pass


class RaceUpdate(BaseModel):
    race_date: Optional[datetime] = None
    track: Optional[str] = None
    distance: Optional[int] = Field(None, ge=0)
    race_type: Optional[str] = None
    class_rating: Optional[int] = None
    total_runners: Optional[int] = None


class RaceRead(RaceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RacesList(BaseModel):
    races: List[RaceRead]


# -------------------- Horse Schemas --------------------
class HorseBase(BaseModel):
    name: str
    jockey: str | None = None
    trainer: str | None = None
    odds: float | None = None
    starting_position: int | None = None
    weight: float | None = None
    last_race_days: int | None = None
    wins: int | None = None
    places: int | None = None
    starts: int | None = None
    avg_position: float | None = None


class HorseCreate(HorseBase):
    race_id: int


class HorseUpdate(BaseModel):
    name: str | None = None
    jockey: str | None = None
    trainer: str | None = None
    odds: float | None = None
    starting_position: int | None = None
    weight: float | None = None
    last_race_days: int | None = None
    wins: int | None = None
    places: int | None = None
    starts: int | None = None
    avg_position: float | None = None


class HorseRead(HorseBase):
    id: int
    race_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
