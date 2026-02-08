from sqlmodel import SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as AsyncSessionMaker
from sqlalchemy import create_engine as sync_create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine for async operations (currently broken due to greenlet)
async_engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Create sync engine for all operations (workaround for greenlet issue)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
sync_engine = sync_create_engine(SYNC_DATABASE_URL, echo=True, pool_pre_ping=True)

# Create sync session maker
SyncSessionMaker = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)


async def create_db_and_tables():
    """Create database tables synchronously to avoid greenlet issues."""

    # ✅ IMPORTANT: Import models so SQLModel registers them
    from src.models.task import Task

    print("Creating tables...")
    # Use sync engine to create tables to avoid greenlet issues
    SQLModel.metadata.create_all(sync_engine)
    print("Tables created successfully!")


async def get_session():
    async with AsyncSessionMaker(async_engine) as session:
        yield session


def get_sync_session():
    """Get a synchronous database session (workaround for greenlet issue on Python 3.13)."""
    with SyncSessionMaker() as session:
        yield session
