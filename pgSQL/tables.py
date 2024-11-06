from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os

import config


DATABASE_URL = config.DB_URL
engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
)

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    uid: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int | None]
    email: Mapped[str | None]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def remove_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main():
    await remove_tables()
    await create_tables()


if __name__ == '__main__':
    asyncio.run(main())