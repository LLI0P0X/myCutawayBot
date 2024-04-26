from aiogram import types, Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
import strConfig

router = Router()

bot = Bot(token=config.BOT_TOKEN)


@router.message(Command("start"))
async def start_handler(msg: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Приветственное сообщение",
        callback_data=f"btnHello")
    )
    if msg.chat.id in [config.TOP_ADMINS]:
        hi = "Добро пожаловать, админ"
    else:
        hi = strConfig.helloMessage + '\n' + msg.chat.id

    await msg.answer(hi, reply_markup=builder.as_markup())


@router.callback_query(lambda c: "btnHello" in c.data)
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Приветственное сообщение",
        callback_data=f"btnHello")
    )
    await callback.message.answer(strConfig.helloMessage, reply_markup=builder.as_markup(),
                                  reply_to_message_id=callback.message.message_id)
