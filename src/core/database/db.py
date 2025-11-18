from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.core.settings.settings import settings


# создаём engine
Base = declarative_base()
engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)
Base.metadata.bind = engine

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)

# dependency для FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
