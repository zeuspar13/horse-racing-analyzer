import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()


@lru_cache()
def get_database_url() -> str:
    """Fetch the database URL from the environment.
    Defaults to a local Postgres instance if not set.
    """
    return os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/horse_racing",
    )


def create_db_engine() -> Engine:
    """Create and return a SQLAlchemy engine."""
    return create_engine(get_database_url(), pool_pre_ping=True, echo=False)


# Global engine and session factory
ENGINE: Engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


def get_db():
    """FastAPI dependency that yields a database session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
