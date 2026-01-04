from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from settings import Settings

settings = Settings()

engine = create_async_engine(url=settings.db_url,future=True,
                             echo=True,
                             pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

async def session_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
