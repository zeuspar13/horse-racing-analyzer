from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    race_date = Column(DateTime)
    track = Column(String)
    distance = Column(Integer)  # metres
    race_type = Column(String)
    class_rating = Column(Integer)
    total_runners = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    horses = relationship("Horse", back_populates="race", cascade="all, delete-orphan")
    analysis = relationship("RaceAnalysis", back_populates="race", uselist=False, cascade="all, delete-orphan")

class Horse(Base):
    __tablename__ = "horses"

    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id"))
    name = Column(String)
    jockey = Column(String)
    trainer = Column(String)
    odds = Column(Float)
    starting_position = Column(Integer)
    weight = Column(Float)  # kg
    last_race_days = Column(Integer)
    wins = Column(Integer)
    places = Column(Integer)
    starts = Column(Integer)
    avg_position = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    race = relationship("Race", back_populates="horses")

class RaceAnalysis(Base):
    __tablename__ = "race_analysis"

    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id"), unique=True)
    winner_prediction = Column(String)
    confidence_score = Column(Float)
    stake_recommendation = Column(Float)
    expected_profit = Column(Float)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    race = relationship("Race", back_populates="analysis")

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id"))
    horse_id = Column(Integer, ForeignKey("horses.id"))
    stake = Column(Float)
    odds = Column(Float)
    bet_type = Column(String)  # WIN, PLACE, EACH_WAY
    placed_at = Column(DateTime, default=datetime.utcnow)
    result = Column(String)  # WON, LOST, PENDING
    profit = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    race = relationship("Race")
    horse = relationship("Horse")

class Bankroll(Base):
    __tablename__ = "bankroll"

    id = Column(Integer, primary_key=True, index=True)
    current_amount = Column(Float)
    initial_amount = Column(Float)
    max_drawdown = Column(Float)
    daily_limit = Column(Float)
    weekly_limit = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RiskParameter(Base):
    __tablename__ = "risk_parameters"

    id = Column(Integer, primary_key=True, index=True)
    confidence_threshold = Column(Float)
    max_stake_percentage = Column(Float)
    correlation_threshold = Column(Float)
    stop_loss_daily = Column(Float)
    stop_loss_weekly = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
