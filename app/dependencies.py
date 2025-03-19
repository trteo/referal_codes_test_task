from typing import Generator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import User
from settings.config import get_db_url, settings


async def get_session() -> Generator[AsyncSession, None, None]:
    engine = create_async_engine(
        get_db_url(settings.POSTGRES_DATABASE),
        echo=False,
        future=True,
    )
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
