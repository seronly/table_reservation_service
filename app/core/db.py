import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

logger = logging.getLogger(__name__)

Base = declarative_base()
engine = create_async_engine(
        url=settings.db_dsn,
        echo=settings.debug,
        echo_pool=settings.debug,
        pool_pre_ping=settings.db_pool_pre_ping,
    )
async_sessionmaker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)

async def  create_session():
    """Create async session
    """
    logger.info("Creating session")
    async with async_sessionmaker() as session:
        logger.info("Session initialized")
        yield session
        logger.info("Session closed")