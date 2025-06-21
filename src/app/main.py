from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db, ENGINE
from . import models, schemas

# Create tables if they don't exist (simple approach for early dev)
models.Base.metadata.create_all(bind=ENGINE)

app = FastAPI(title="Horse Racing Betting Analyzer", version="0.1.0")


@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}


@app.post("/races", response_model=schemas.RaceRead, status_code=status.HTTP_201_CREATED, tags=["Races"])
def create_race(race_in: schemas.RaceCreate, db: Session = Depends(get_db)):
    race = models.Race(**race_in.model_dump())
    db.add(race)
    db.commit()
    db.refresh(race)
    return race


@app.get("/races", response_model=list[schemas.RaceRead], tags=["Races"])
def list_races(db: Session = Depends(get_db)):
    return db.query(models.Race).all()


@app.get("/races/{race_id}", response_model=schemas.RaceRead, tags=["Races"])
def get_race(race_id: int, db: Session = Depends(get_db)):
    race = db.get(models.Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


@app.put("/races/{race_id}", response_model=schemas.RaceRead, tags=["Races"])
def update_race(race_id: int, race_in: schemas.RaceUpdate, db: Session = Depends(get_db)):
    race = db.get(models.Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    for field, value in race_in.model_dump(exclude_unset=True).items():
        setattr(race, field, value)
    db.commit()
    db.refresh(race)
    return race


@app.delete("/races/{race_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Races"])
def delete_race(race_id: int, db: Session = Depends(get_db)):
    race = db.get(models.Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    db.delete(race)
    db.commit()
    return None
