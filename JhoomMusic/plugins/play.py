import asyncio
import os
import yt_dlp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import is_music_playing, music_on, music_off
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.inline.play import stream_markup, telegram_markup
from JhoomMusic.utils.stream import stream
from config import BANNED_USERS

@app.on_message(
    filters.command(["play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def play_commnd(client, message: Message, _, chat_id):
    if len(message.command) < 2:
        return await message.reply_text(_["play_1"])
    
    if message.sender_chat:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="How to Fix this?",
                        callback_data="AnonymousAdmin",
                    ),
                ]
            ]
        )
        return await message.reply_text(
            _["general_4"], reply_markup=upl
        )
    
    if await is_music_playing(chat_id):
        await music_off(chat_id)
    
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url, videoid=True):
            return await message.reply_text(_["play_3"])
        
        mystic = await message.reply_text(_["play_6"])
        
        try:
            details, track_details = await YouTube.track(url, True)
        except Exception:
            return await mystic.edit_text(_["play_3"])
        
        streamtype = "video" if message.command[0][0] == "v" else "audio"
        
        if streamtype == "video":
            quality = await get_video_limit(chat_id)
        else:
            quality = "audio"
        
        try:
            await stream(
                _,
                mystic,
                message.from_user.id,
                details,
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                streamtype,
                quality,
                forceplay=message.command[0][-5:] == "force",
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            return await mystic.edit_text(err)
        
        return await mystic.delete()
    else:
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text(_["play_1"])
        
        try:
            results = await YouTube.search(query)
        except:
            return await mystic.edit_text(_["play_5"])
        
        if not results:
            return await mystic.edit_text(_["play_4"])
        
        buttons = []
        for i, result in enumerate(results[:5]):
            buttons.append([
                InlineKeyboardButton(
                    text=f"{i+1}. {result['title'][:30]}...",
                    callback_data=f"MusicStream {result['link']}|{streamtype}|{message.from_user.id}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {message.from_user.id}|{chat_id}"
            )
        ])
        
        await mystic.edit_text(
            _["play_7"],
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    
    await music_on(chat_id)
    await Jhoom.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention)
    )

@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    
    await music_off(chat_id)
    await Jhoom.resume_stream(chat_id)
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention)
    )

@app.on_message(filters.command(["stop", "end", "cstop", "cend"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def stop_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    
    await Jhoom.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_9"].format(message.from_user.mention)
    )

@app.on_message(filters.command(["skip", "cskip"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def skip_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
    
    popped = None
    try:
        popped = check.pop(0)
        if popped:
            await auto_clean(popped)
        if not check:
            await Jhoom.stop_stream(chat_id)
            await set_loop(chat_id, 0)
            return await message.reply_text(
                _["admin_10"].format(message.from_user.mention)
            )
        else:
            await Jhoom.skip_stream(chat_id, check[0]["file"])
    except:
        try:
            await Jhoom.stop_stream(chat_id)
            await set_loop(chat_id, 0)
        except:
            pass
        return await message.reply_text(
            _["admin_10"].format(message.from_user.mention)
        )
    
    await message.reply_text(
        _["admin_11"].format(message.from_user.mention)
    )

@app.on_message(filters.command(["shuffle", "cshuffle"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def shuffle_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
    
    try:
        popped = check.pop(0)
    except:
        return await message.reply_text(_["queue_2"])
    
    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        return await message.reply_text(_["admin_16"])
    
    random.shuffle(check)
    check.insert(0, popped)
    await message.reply_text(
        _["admin_13"].format(message.from_user.mention)
    )

@app.on_message(filters.command(["loop", "cloop"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def loop_command(client, message: Message, _, chat_id):
    if len(message.command) != 2:
        return await message.reply_text(_["admin_17"])
    
    state = message.text.split(None, 1)[1].strip()
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if state > 10:
                state = 10
            await set_loop(chat_id, state)
            return await message.reply_text(
                _["admin_18"].format(
                    message.from_user.mention, state
                )
            )
        else:
            return await message.reply_text(_["admin_17"])
    
    if state.lower() == "enable":
        await set_loop(chat_id, 10)
        return await message.reply_text(
            _["admin_19"].format(message.from_user.mention)
        )
    elif state.lower() == "disable":
        await set_loop(chat_id, 0)
        return await message.reply_text(
            _["admin_20"].format(message.from_user.mention)
        )
    else:
        return await message.reply_text(_["admin_17"])