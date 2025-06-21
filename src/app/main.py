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


# -------------------- Horse Routes --------------------
@app.post("/horses", response_model=schemas.HorseRead, status_code=status.HTTP_201_CREATED, tags=["Horses"])
def create_horse(horse_in: schemas.HorseCreate, db: Session = Depends(get_db)):
     # Ensure race exists
     race = db.get(models.Race, horse_in.race_id)
     if not race:
         raise HTTPException(status_code=404, detail="Race not found")

     horse = models.Horse(**horse_in.model_dump())
     db.add(horse)
     db.commit()
     db.refresh(horse)
     return horse


@app.get("/horses", response_model=list[schemas.HorseRead], tags=["Horses"])
def list_horses(db: Session = Depends(get_db)):
     return db.query(models.Horse).all()


@app.get("/horses/{horse_id}", response_model=schemas.HorseRead, tags=["Horses"])
def get_horse(horse_id: int, db: Session = Depends(get_db)):
     horse = db.get(models.Horse, horse_id)
     if not horse:
         raise HTTPException(status_code=404, detail="Horse not found")
     return horse


@app.put("/horses/{horse_id}", response_model=schemas.HorseRead, tags=["Horses"])
def update_horse(horse_id: int, horse_in: schemas.HorseUpdate, db: Session = Depends(get_db)):
     horse = db.get(models.Horse, horse_id)
     if not horse:
         raise HTTPException(status_code=404, detail="Horse not found")
     for field, value in horse_in.model_dump(exclude_unset=True).items():
         setattr(horse, field, value)
     db.commit()
     db.refresh(horse)
     return horse


@app.delete("/horses/{horse_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Horses"])
def delete_horse(horse_id: int, db: Session = Depends(get_db)):
     horse = db.get(models.Horse, horse_id)
     if not horse:
         raise HTTPException(status_code=404, detail="Horse not found")
     db.delete(horse)
     db.commit()
     return None
