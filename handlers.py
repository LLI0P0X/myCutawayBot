import datetime
import asyncio
import aiogram

from aiogram import types, Bot, Router
from aiogram.types import Message, CallbackQuery, MessageReactionUpdated, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

import config
import strConfig
import CD.myService, CD.myGitHab
from utils import myMath
import sqla

from myLogger import logger

router = Router()

bot = Bot(token=config.BOT_TOKEN)


async def send_and_remove(msg: Message, text: str, parse_mode=None, reply_markup=None, time=5):
    nmsg = await msg.answer(text, parse_mode=parse_mode, reply_markup=reply_markup)
    await asyncio.sleep(time)
    await bot.delete_message(nmsg.chat.id, nmsg.message_id)


def parse_args(inp: Message | CallbackQuery):
    if type(inp) is Message:
        _uid = inp.from_user.id
        _args = inp.text.split(' ')
    else:
        _uid = inp.from_user.id
        _args = inp.data.split(' ')
    return _uid, _args


@router.message(Command("start"))
async def hello_handler(msg: Message):
    builder = InlineKeyboardBuilder()
    if str(msg.from_user.id) in config.TOP_ADMINS:
        hi = "Добро пожаловать, админ"
        builder.add(types.InlineKeyboardButton(
            text=f"Приветственное сообщение",
            callback_data=f"btnHello")
        )
    else:
        hi = strConfig.helloMessage
    logger.debug(str(msg))
    if not await sqla.check_user_by_tg_id(msg.from_user.id):
        user = {
            'tg_id': msg.from_user.id,
        }
        if msg.from_user.first_name:
            user['name'] = msg.from_user.first_name
        await sqla.add_user(**user)
    await msg.answer(hi, reply_markup=builder.as_markup())


@router.message(Command("dev"))
async def dev_handler(msg: Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    if msg.reply_to_message:
        logger.debug(msg.reply_to_message.html_text)
    else:
        await send_and_remove(msg, '<b>bold</b>\n'
                                   '<i>italic</i>\n'
                                   '<u>underline</u>\n'
                                   '<s>strikethrough</s>\n'
                                   '<tg-spoiler>spoiler</tg-spoiler>', parse_mode='html')


@router.message(Command("menu"))
@router.message(Command("m"))
@router.callback_query(F.data.contains('startMenu'))
async def menu_handler(msg: Message | types.CallbackQuery):
    await bot.delete_message(msg.chat.id, msg.message_id)
    builder = InlineKeyboardBuilder()
    _uid, _args = parse_args(msg)
    builder.add(types.InlineKeyboardButton(
        text='Приветствие',
        callback_data='startMenu -> btnHello'
    ))
    if len(_args) == 1:
        await msg.answer(strConfig.menuMessages['start'], reply_markup=builder.as_markup())


@router.message(Command("важно"))
@router.message(Command("important"))
@router.message(Command("i"))
async def important_handler(msg: Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    logger.debug(msg)
    _uid, _args = parse_args(msg)
    if msg.reply_to_message:
        text = msg.reply_to_message.html_text
        html_msg = f'<b>Важное сообщение от @{msg.from_user.username}</b>\n'
        html_msg += text + '\n'
        html_msg += f'#Важное'
        logger.debug(text)
        await bot.send_message(msg.chat.id, html_msg, disable_notification=True, parse_mode='html')
    else:
        await send_and_remove(msg, 'Нет выделенного сообщения')


@router.message(Command("заметка"))
@router.message(Command("note"))
@router.message(Command("n"))
async def note_handler(msg: Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    logger.debug(msg)
    _uid, _args = parse_args(msg)
    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id == bot.id and \
                msg.reply_to_message.html_text[:23] == '<b>Важное сообщение от ':
            rmsg_html = dict()
            rmsg_html['all'] = msg.reply_to_message.html_text.split('\n')
            rmsg_html['title'] = rmsg_html['all'][0]
            rmsg_html['text'] = rmsg_html['all'][1:-1]
            if '<tg-spoiler>Заметки:</tg-spoiler>' in rmsg_html['all']:
                ind = rmsg_html['all'][::-1].index('<tg-spoiler>Заметки:</tg-spoiler>')
                rmsg_html['notes'] = rmsg_html['all'][-ind:-1]
                rmsg_html['text'].remove('<tg-spoiler>Заметки:</tg-spoiler>')
                for note in rmsg_html['notes']:
                    rmsg_html['text'].remove(note)
            else:
                rmsg_html['notes'] = []
            rmsg_html['tags'] = rmsg_html['all'][-1]

            if _args[1] in ['dell', 'd', 'remove', 'r'] and len(_args) > 2:
                try:
                    rmsg_html['notes'].pop(int(_args[2]) - 1)
                except IndexError:
                    await send_and_remove(msg, 'Нет заметки с таким номером')
                except ValueError:
                    await send_and_remove(msg, 'Формат: \n'
                                               '/note add <текст заметки> -- для добавления заметки\n'
                                               '/note dell <номер заметки> -- для удаления заметки\n')
            elif _args[1] in ['add']:
                rmsg_html['notes'].append(f"<tg-spoiler>{''.join(_arg + ' ' for _arg in _args[2:])}</tg-spoiler>")
            elif len(_args) > 1:
                rmsg_html['notes'].append(f"<tg-spoiler>{''.join(_arg + ' ' for _arg in _args[1:])}</tg-spoiler>")
                await send_and_remove(msg, f'Заметка добавлена: ')
            else:
                await send_and_remove(msg, 'Формат: \n'
                                           '/note add <текст заметки> -- для добавления заметки\n'
                                           '/note dell <номер заметки> -- для удаления заметки\n')
                return None

            rmsg_html['new'] = rmsg_html['title']
            for text in rmsg_html['text']:
                rmsg_html['new'] += '\n' + text
            if len(rmsg_html['notes']) > 0:
                rmsg_html['new'] += '\n<tg-spoiler>Заметки:</tg-spoiler>'
                for note in rmsg_html['notes']:
                    rmsg_html['new'] += '\n' + note
            rmsg_html['new'] += '\n' + rmsg_html['tags']
            logger.debug(rmsg_html['new'])
            await bot.edit_message_text(chat_id=msg.chat.id,
                                        message_id=msg.reply_to_message.message_id,
                                        text=rmsg_html['new'],
                                        parse_mode='html')
        else:
            await send_and_remove(msg, 'Заметки можно оставлять только на <b>важные сообщения</b>', parse_mode='html')
    else:
        await send_and_remove(msg, 'Нет выделенного сообщения')


@router.message(Command("tag"))
@router.message(Command("t"))
async def tag_handler(msg: Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    logger.debug(msg)
    _uid, _args = parse_args(msg)
    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id == bot.id and \
                msg.reply_to_message.html_text[:23] == '<b>Важное сообщение от ':
            if len(_args) == 2:
                rmsg_html = dict()
                rmsg_html['all'] = msg.reply_to_message.html_text.split('\n')[:-1]
                rmsg_html['tag'] = f'#{_args[1]}'

                rmsg_html['new'] = rmsg_html['all'][0]
                for text in rmsg_html['all'][1:]:
                    rmsg_html['new'] += '\n' + text
                rmsg_html['new'] += '\n' + rmsg_html['tag']

                await bot.edit_message_text(chat_id=msg.chat.id,
                                            message_id=msg.reply_to_message.message_id,
                                            text=rmsg_html['new'],
                                            parse_mode='html')

            else:
                await send_and_remove(msg, 'Формат: \n'
                                           '/tag <текст тега (одно слово)> -- для изменения тега')
        else:
            await send_and_remove(msg, 'Тег можно оставлять только на <b>важные сообщения</b>', parse_mode='html')
    else:
        await send_and_remove(msg, 'Нет выделенного сообщения')


@router.message(Command("cd_run"))
async def upg_handler(msg: Message):
    if str(msg.from_user.id) in config.TOP_ADMINS:
        await msg.answer('Обновление начато')
        CD.myGitHab.pull()
        # CD.myService.createService('main')
        CD.myService.runService('main')
    else:
        await msg.answer(strConfig.accessDenied + '\n id: ' + str(msg.from_user.id))


@router.message(Command("euler"))
async def euler_handler(msg: Message):
    n = msg.text.split(' ')[1]
    ret = myMath.eulerFunctionFull(n)
    ans = str(ret['res'])
    ans += '\n'
    ans += n
    for i in ret['all']:
        ans += f'*(1-1/{i})'
    ans += f'={ret["res"]}'
    await msg.answer(ans)


@router.message(Command("canonical"))
async def canonical_handler(msg: Message):
    n = msg.text.split(' ')[1]
    ret = myMath.canonicalNumber(n)
    await msg.answer(ret)


@router.callback_query(F.data == "btnHello")
async def hi_handler(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    await callback.message.answer(strConfig.helloMessage, reply_markup=builder.as_markup(),
                                  reply_to_message_id=callback.message.message_id)


@router.message()
async def other_messages(msg: Message):
    if msg.chat.type == 'private':
        logger.warning(f'Неизвестная команда от {msg.from_user.username}: {msg.text}')
        await msg.answer('Неизвестная команда')
    else:
        await sqla.add_tg_need_delete_message(msg.chat.id, msg.message_id,
                                              date=datetime.datetime.now() + datetime.timedelta(seconds=10))
        for needRemove in await sqla.get_tg_need_delete_messages():
            try:
                await bot.delete_message(needRemove.chat_id, needRemove.message_id)
            except aiogram.exceptions.TelegramBadRequest:
                pass
            finally:
                await sqla.remove_tg_need_delete_message(needRemove[0])


@router.message_reaction()
async def other_reaction(msg: MessageReactionUpdated):
    if msg.chat.type == 'private':
        logger.debug(msg)
        logger.warning(f'Неизвестная реакция от {msg.user.username}: {msg.old_reaction} => {msg.new_reaction}')
        await bot.send_message(msg.chat.id, 'Неизвестная реакция')


@router.callback_query()
async def other_callback(callback: types.CallbackQuery):
    logger.warning(f'Неизвестная callback от {callback.from_user}: {callback.data}')
    # await callback.answer('Неизвестная команда')
