from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os

import config

import tables
from tables import engine, Users


async def add_user(**kwargs):
    async with engine.begin() as conn:
        await conn.execute(
            insert(Users).values(**kwargs))


async def select_users():
    async with engine.begin() as conn:
        result = await conn.execute(select(Users))
        return result.fetchall()


async def main():
    await add_user(tg_id=123)
    print(await select_users())


if __name__ == "__main__":
    asyncio.run(main())
