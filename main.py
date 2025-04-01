import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
import strConfig
from handlers import router
from myLogger import logger


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logger.notify_sync('INFO', strConfig.startMsgForAdm)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical('Bot stopped by user')
