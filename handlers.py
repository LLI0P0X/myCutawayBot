from aiogram import types, Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
import strConfig
import CD.myService, CD.myGitHab

router = Router()

bot = Bot(token=config.BOT_TOKEN)


@router.message(Command("start"))
async def start_handler(msg: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Приветственное сообщение",
        callback_data=f"btnHello")
    )
    if msg.chat.id in config.TOP_ADMINS:
        hi = "Добро пожаловать, админ"
    else:
        hi = strConfig.helloMessage

    await msg.answer(hi, reply_markup=builder.as_markup())


@router.message(Command("cd_run"))
async def start_handler(msg: Message):
    if msg.chat.id in config.TOP_ADMINS:
        await msg.answer('Обновление начато')
        CD.myGitHab.pull()
        CD.myService.createService('main')
        CD.myService.runService('main')
    else:
        await msg.answer(strConfig.accessDenied + '\n id: ' + str(msg.chat.id))


@router.callback_query(lambda c: "btnHello" in c.data)
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Приветственное сообщение",
        callback_data=f"btnHello")
    )
    await callback.message.answer(strConfig.helloMessage, reply_markup=builder.as_markup(),
                                  reply_to_message_id=callback.message.message_id)
