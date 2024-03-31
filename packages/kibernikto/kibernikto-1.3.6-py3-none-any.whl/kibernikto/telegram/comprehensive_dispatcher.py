import logging
import os
import sys
import traceback
from random import choice
from typing import List

from aiogram import Bot, Dispatcher, types, enums, F
from aiogram.filters import or_f
from aiogram.types import User
from pydantic_settings import BaseSettings

from kibernikto.interactors import OpenAiExecutorConfig
from kibernikto.interactors.tools import Toolbox
from kibernikto.utils.text import split_text_by_sentences
from ._executor_corral import init as init_ai_bot_corral, get_ai_executor, kill as kill_animals
from ._message_preprocessors import get_message_text
from .telegram_bot import TelegramBot


class TelegramSettings(BaseSettings):
    TG_BOT_KEY: str
    TG_MASTER_ID: int
    TG_MASTER_IDS: list = []
    TG_FRIEND_GROUP_IDS: list = []
    TG_MAX_MESSAGE_LENGTH: int = 4096
    TG_CHUNK_SENTENCES: int = 7
    TG_REACTION_CALLS: List[str] = ['honda', 'киберникто']
    TG_SAY_HI: bool = False
    TG_STICKER_LIST: List[str] = ()


TELEGRAM_SETTINGS = TelegramSettings()

smart_bot_class = None
TOOLS: List[Toolbox] = []

# Telegram bot
tg_bot: Bot = None
bot_me: User = None
dp = Dispatcher()

commands = {}


def start(bot_class, tools=[]):
    """
    runs the executor polling the dispatcher for incoming messages

    :param bot_class: the bot class to use
    :return:
    """
    global smart_bot_class
    global tg_bot
    global TOOLS
    TOOLS = tools
    smart_bot_class = bot_class
    dp.startup.register(on_startup)
    tg_bot = Bot(token=TELEGRAM_SETTINGS.TG_BOT_KEY)
    dp.run_polling(tg_bot, skip_updates=True)


async def on_startup(bot: Bot):
    try:
        global bot_me

        if bot_me is None:
            bot_me = await bot.get_me()

        executor_config = OpenAiExecutorConfig(name=bot_me.first_name,
                                               reaction_calls=TELEGRAM_SETTINGS.TG_REACTION_CALLS,
                                               tools=TOOLS)

        bot_cfg = {
            "config": executor_config,
            "master_id": TELEGRAM_SETTINGS.TG_MASTER_IDS,
            "username": bot_me.username
        }

        init_ai_bot_corral(smart_bot_class=smart_bot_class,
                           master_id=TELEGRAM_SETTINGS.TG_MASTER_ID,
                           username=bot_me.username,
                           config=bot_cfg)

        if TELEGRAM_SETTINGS.TG_SAY_HI and TELEGRAM_SETTINGS.TG_MASTER_IDS:
            master_id = TELEGRAM_SETTINGS.TG_MASTER_IDS[0]
            await send_random_sticker(chat_id=master_id)
            bot: TelegramBot = get_ai_executor(master_id)
            hi_message = await bot.heed_and_reply("Поприветствуй своего хозяина!",
                                                  save_to_history=False)
            await tg_bot.send_message(chat_id=master_id, text=hi_message)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        logging.error(f"failed to start! \n{str(e)}")
        await kill_animals()
        await dp.stop_polling()
        exit(os.EX_CONFIG)


async def send_random_sticker(chat_id):
    sticker_id = choice(TELEGRAM_SETTINGS.TG_STICKER_LIST)

    # say hi to everyone
    await tg_bot.send_sticker(
        sticker=sticker_id,
        chat_id=chat_id)


@dp.message(F.chat.type == enums.ChatType.PRIVATE)
async def private_message(message: types.Message):
    user_id = message.from_user.id

    if TELEGRAM_SETTINGS.TG_MASTER_IDS and user_id not in TELEGRAM_SETTINGS.TG_MASTER_IDS:
        negative_reply_text = f"Я не отвечаю на вопросы в личных беседах с незакомыми людьми (если это конечно не один из моиз Повелителей " \
                              f"снизошёл до меня). Я передам ваше соообщение мастеру."
        await tg_bot.send_message(user_id,
                                  negative_reply_text)
        await tg_bot.send_message(TELEGRAM_SETTINGS.TG_MASTER_IDS[0],
                                  f"{message.from_user.username}: {message.md_text}")

    user_text = await get_message_text(message, tg_bot=tg_bot)

    user_ai = get_ai_executor(user_id)

    await tg_bot.send_chat_action(message.chat.id, 'typing')
    reply_text = await user_ai.heed_and_reply(message=user_text)

    chunks = split_text_by_sentences(reply_text, TELEGRAM_SETTINGS.TG_MAX_MESSAGE_LENGTH)
    for chunk in chunks:
        await message.reply(text=chunk)


@dp.message(or_f(F.chat.type == enums.ChatType.GROUP, F.chat.type == enums.ChatType.SUPERGROUP))
async def group_message(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if TELEGRAM_SETTINGS.TG_FRIEND_GROUP_IDS and chat_id not in TELEGRAM_SETTINGS.TG_FRIEND_GROUP_IDS:
        negative_reply_text = (f"Я не общаюсь в беседах, в которых мне не велено участвовать"
                               f" (если это конечно не один из моих Повелителей"
                               f" снизошёл до меня). Я передам ваше соообщение кому-нибудь.")
        await tg_bot.send_message(user_id,
                                  negative_reply_text)
        await tg_bot.send_message(TELEGRAM_SETTINGS.TG_MASTER_IDS[0],
                                  f"{message.from_user.username}: {message.md_text}")

    user_text = await get_message_text(message)
    group_ai = get_ai_executor(user_id)

    if is_reply(message) or group_ai.should_react(message.md_text):
        await tg_bot.send_chat_action(message.chat.id, 'typing')
        reply_text = await group_ai.heed_and_reply(message=user_text)

        chunks = split_text_by_sentences(reply_text, TELEGRAM_SETTINGS.TG_MAX_MESSAGE_LENGTH)
        for chunk in chunks:
            await message.reply(text=chunk)


def is_reply(message: types.Message):
    if message.reply_to_message and message.reply_to_message.from_user.id == tg_bot.id:
        return True
