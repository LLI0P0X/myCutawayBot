from aiogram import types, Bot, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

import config
import strConfig
import CD.myService, CD.myGitHab
from utils import myMath

router = Router()

bot = Bot(token=config.BOT_TOKEN)


@router.message(Command("start"))
async def hello_handler(msg: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Приветственное сообщение",
        callback_data=f"btnHello")
    )
    if str(msg.from_user.id) in config.TOP_ADMINS:
        hi = "Добро пожаловать, админ"
    else:
        hi = strConfig.helloMessage

    await msg.answer(hi, reply_markup=builder.as_markup())


@router.message(Command("dev"))
async def dev_handler(msg: Message):
    await msg.answer('dev ok 06.11.2024 -changed')

@router.message(Command("cd_run"))
async def upg_handler(msg: Message):
    if str(msg.from_user.id) in config.TOP_ADMINS:
        await msg.answer('Обновление начато')
        CD.myGitHab.pull()
        # CD.myService.createService('main')
        CD.myService.runService('main')
    else:
        await msg.answer(strConfig.accessDenied + '\n id: ' + str(msg.from_user.id))


@router.message(Command("l"))
async def eulers_handler(msg: Message):
    n = msg.text.split(' ')[1]
    ret = myMath.eulersFunctionFull(n)
    ans = str(ret['res'])
    ans += '\n'
    ans += n
    for i in ret['all']:
        ans += f'*(1-1/{i})'
    ans += f'={ret["res"]}'
    await msg.answer(ans)


@router.message(Command("con"))
async def cononical_handler(msg: Message):
    n = msg.text.split(' ')[1]
    ret = myMath.cononicalNumber(n)
    await msg.answer(ret)


@router.callback_query(F.data("btnHello"))
async def hi_handler(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Приветственное сообщение",
        callback_data=f"btnHello")
    )
    await callback.message.answer(strConfig.helloMessage, reply_markup=builder.as_markup(),
                                  reply_to_message_id=callback.message.message_id)
