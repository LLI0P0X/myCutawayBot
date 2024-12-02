from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, update, select, delete
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os
import subprocess

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
    instagram: Mapped[str | None]
    phone: Mapped[str | None]
    name: Mapped[str | None]
    balance: Mapped[float | None]


class Messages(Base):
    __tablename__ = 'messages'
    mid: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[int] = mapped_column(ForeignKey('users.uid', ondelete='CASCADE'))
    role: Mapped[str]
    message: Mapped[str]
    timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    inWork: Mapped[bool] = mapped_column(default=False)
    needWork: Mapped[bool] = mapped_column(default=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def remove_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def run_alembic():
    subprocess.run('alembic revision --autogenerate', shell=True)
    subprocess.run('alembic upgrade head', shell=True)


async def add_user(**kwargs):
    async with engine.begin() as conn:
        await conn.execute(
            insert(Users).values(**kwargs))


async def check_user_by_tg_id(tg_id):
    async with engine.begin() as conn:
        result = await conn.execute(select(Users).where(Users.tg_id == tg_id))
        if result.fetchall():
            return True
        else:
            return False


async def select_users():
    async with engine.begin() as conn:
        result = await conn.execute(select(Users))
        return result.fetchall()


async def main():
    # await remove_tables()
    # await create_tables()
    run_alembic()
    # print(await select_users())
    # print(await check_user_by_tg_id(123))


if __name__ == '__main__':
    asyncio.run(main())