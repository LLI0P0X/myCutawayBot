import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
import strConfig
from handlers import router


async def startMsg():
    bot = Bot(token=config.BOT_TOKEN)
    for ids in config.TOP_ADMINS:
        await bot.send_message(ids, strConfig.startMsgForAdm)
    await bot.session.close()


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), on_startup=startMsg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
