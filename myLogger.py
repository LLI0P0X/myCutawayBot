import asyncio
import logging
import os
import datetime
import inspect

from loguru import _logger
from loguru import _defaults

import atexit as _atexit
import sys as _sys

__all__ = ["logger"]


def getDepth(frame):
    depth = 0
    while frame.f_code.co_filename in [logging.__file__, __file__]:
        frame = frame.f_back
        depth += 1
    return depth


class MyLogger(_logger.Logger):
    def __init__(self,
                 tg_notify=False,
                 tg_token=None,
                 tg_ids=[],
                 core=_logger.Core(),
                 exception=None,
                 depth=0,
                 record=False,
                 lazy=False,
                 colors=False,
                 raw=False,
                 capture=True,
                 patchers=[],
                 extra={},
                 ):
        super(MyLogger, self).__init__(core, exception, depth, record, lazy, colors, raw, capture, patchers, extra)
        self.tg_notify = tg_notify
        if tg_notify:
            from aiogram import Bot
            import asyncio
            if tg_token:
                self.bot = Bot(token=tg_token)
            else:
                try:
                    import config
                    self.bot = Bot(token=config.BOT_TOKEN)
                except ImportError | ModuleNotFoundError | AttributeError:
                    self.warning('No tg_token provided, tg_notify is set to False')
                    self.tg_notify = False
            if tg_ids:
                self.tg_ids = tg_ids
            else:
                try:
                    import config
                    self.tg_ids = config.TOP_ADMINS
                except ImportError | ModuleNotFoundError | AttributeError:
                    self.warning('No tg_ids provided, tg_notify is set to False')
                    self.tg_notify = False

    def opt_log(self, level, message, *args, **kwargs):
        depth = getDepth(inspect.currentframe())
        super().opt(depth=depth).log(level, message, *args, **kwargs)

    def notify_sync(self, level, message):
        if self.tg_notify:
            # self.log(level, message)
            msg = f"lvl: {level}\nserver time:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}"
            for _id in self.tg_ids:
                asyncio.run(self.bot.send_message(_id, msg))
        else:
            self.warning('tg_notify is False')
        self.opt_log(level, message)

    async def notify(self, level, message):
        if self.tg_notify:
            msg = f"lvl: {level}\nserver time:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}"
            for _id in self.tg_ids:
                await self.bot.send_message(_id, msg)
        else:
            self.warning('tg_notify is False')
        self.opt_log(level, message)


logger = MyLogger(tg_notify=True)
if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    logger.add(_sys.stderr)
_atexit.register(logger.remove)

logDir = os.path.join(os.getcwd(), 'logs')
logPath = os.path.join(logDir, f"log_{datetime.datetime.now().strftime('d%Y-%m-%dt%H-%M-%S')}.log")

logger.add(logPath, mode='w', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", encoding='utf-8',
           rotation="1 MB", compression="zip")


class InterceptHandler(logging.Handler):
    def setupLogger(
            level: str | int = "DEBUG",
            ignored: list[str] = ""
    ):
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=logging.getLevelName(level)
        )
        for ignore in ignored:
            logger.disable(ignore)

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame = logging.currentframe()
        depth = getDepth(frame)
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


InterceptHandler.setupLogger('INFO')

if __name__ == '__main__':
    logger.info('hello logs')
