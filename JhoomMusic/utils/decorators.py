import asyncio
import time
from typing import Callable, Union

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.database import (
    get_lang,
    is_commanddelete_on,
    is_maintenance,
)

def language(mystic):
    async def wrapper(_, message: Message, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = language["language"]
        except:
            language = "en"
        return await mystic(_, message, language, **kwargs)
    return wrapper

def languageCB(mystic):
    async def wrapper(_, CallbackQuery: CallbackQuery, **kwargs):
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            language = language["language"]
        except:
            language = "en"
        return await mystic(_, CallbackQuery, language, **kwargs)
    return wrapper

def ActualAdminCB(mystic):
    async def wrapper(_, CallbackQuery: CallbackQuery, **kwargs):
        if CallbackQuery.message.chat.type == "private":
            return await mystic(_, CallbackQuery, **kwargs)
        
        a = await app.get_chat_member(
            CallbackQuery.message.chat.id, CallbackQuery.from_user.id
        )
        if a.status != "creator":
            if a.status != "administrator":
                if CallbackQuery.from_user.id not in SUDOERS:
                    return await CallbackQuery.answer(
                        "You need to be an admin to use this.", show_alert=True
                    )
        return await mystic(_, CallbackQuery, **kwargs)
    return wrapper

def AdminRightsCheck(mystic):
    async def wrapper(_, message: Message, **kwargs):
        if message.chat.type == "private":
            return await mystic(_, message, **kwargs)
        
        a = await app.get_chat_member(message.chat.id, message.from_user.id)
        if a.status != "creator":
            if a.status != "administrator":
                if message.from_user.id not in SUDOERS:
                    return await message.reply_text(
                        "You need to be an admin to use this command."
                    )
        return await mystic(_, message, **kwargs)
    return wrapper

def AdminActual(mystic):
    async def wrapper(_, message: Message, **kwargs):
        if message.chat.type == "private":
            return await mystic(_, message, **kwargs)
        
        a = await app.get_chat_member(message.chat.id, message.from_user.id)
        if a.status != "creator":
            if a.status != "administrator":
                if message.from_user.id not in SUDOERS:
                    return
        return await mystic(_, message, **kwargs)
    return wrapper
