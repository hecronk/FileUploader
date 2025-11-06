from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.core.settings.settings import settings

# создаём engine
Base = declarative_base()
engine = create_engine(settings.database_url, echo=settings.debug)
Base.metadata.bind = engine

# создаём sessionmaker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
