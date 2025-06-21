from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import get_db, ENGINE
from . import models

# Create tables if they don't exist (simple approach for early dev)
models.Base.metadata.create_all(bind=ENGINE)

app = FastAPI(title="Horse Racing Betting Analyzer", version="0.1.0")


@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}


@app.get("/races", tags=["Races"])
def list_races(db: Session = Depends(get_db)):
    return db.query(models.Race).all()
