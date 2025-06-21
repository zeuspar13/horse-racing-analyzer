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
