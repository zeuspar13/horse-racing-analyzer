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


# -------------------- Bet Schemas --------------------
class BetBase(BaseModel):
    race_id: int
    horse_id: int
    stake: float
    odds: float
    bet_type: str  # WIN, PLACE, EACH_WAY


class BetCreate(BetBase):
    pass


class BetUpdate(BaseModel):
    stake: float | None = None
    odds: float | None = None
    bet_type: str | None = None
    result: str | None = None
    profit: float | None = None


class BetRead(BetBase):
    id: int
    result: str | None = None
    profit: float | None = None
    placed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------- Bankroll Schemas --------------------
class BankrollBase(BaseModel):
    current_amount: float
    initial_amount: float
    max_drawdown: float | None = None
    daily_limit: float | None = None
    weekly_limit: float | None = None


class BankrollCreate(BankrollBase):
    pass


class BankrollUpdate(BaseModel):
    current_amount: float | None = None
    max_drawdown: float | None = None
    daily_limit: float | None = None
    weekly_limit: float | None = None


class BankrollRead(BankrollBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -------------------- Race Analysis Schemas --------------------
class RaceAnalysisBase(BaseModel):
    race_id: int
    winner_prediction: str
    confidence_score: float
    stake_recommendation: float
    expected_profit: float
    analysis_reasoning: str
    risk_assessment: str


class RaceAnalysisCreate(RaceAnalysisBase):
    pass


class RaceAnalysisUpdate(BaseModel):
    winner_prediction: str | None = None
    confidence_score: float | None = None
    stake_recommendation: float | None = None
    expected_profit: float | None = None


class RaceAnalysisRead(RaceAnalysisBase):
    id: int
    analysis_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
