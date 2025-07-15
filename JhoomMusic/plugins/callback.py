import asyncio
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import (
    get_lang, 
    is_music_playing, 
    music_on, 
    music_off,
    get_loop,
    set_loop
)
from JhoomMusic.utils.decorators import languageCB
from JhoomMusic.utils.formatters import seconds_to_min, speed_converter
from JhoomMusic.utils.inline.play import (
    stream_markup,
    telegram_markup,
    close_markup,
    livestream_markup,
    slider_markup,
    panel_markup_1,
    panel_markup_2,
    panel_markup_3
)
from JhoomMusic.utils.stream import stream
from config import BANNED_USERS

@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
async def play_music_callback(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, streamtype, userid = callback_request.split("|")
    
    if CallbackQuery.from_user.id != int(userid):
        try:
            return await CallbackQuery.answer(
                "This is not for you! Search for your own song.",
                show_alert=True,
            )
        except:
            return
    
    await CallbackQuery.answer()
    await CallbackQuery.edit_message_text("**Processing...**")
    
    try:
        details, track_details = await YouTube.track(vidid, True)
    except Exception:
        return await CallbackQuery.edit_message_text("**Failed to get track details.**")
    
    if streamtype == "video":
        quality = await get_video_limit(CallbackQuery.message.chat.id)
    else:
        quality = "audio"
    
    try:
        await stream(
            _,
            CallbackQuery,
            CallbackQuery.from_user.id,
            details,
            CallbackQuery.message.chat.id,
            CallbackQuery.from_user.first_name,
            CallbackQuery.message.chat.id,
            streamtype,
            quality,
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else "**An error occurred.**"
        return await CallbackQuery.edit_message_text(err)
    
    return await CallbackQuery.delete()

@app.on_callback_query(filters.regex("Pages") & ~BANNED_USERS)
async def slider_queries(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, rtype, query, userid = callback_request.split("|")
    
    if CallbackQuery.from_user.id != int(userid):
        try:
            return await CallbackQuery.answer(
                "This is not for you! Search for your own song.",
                show_alert=True,
            )
        except:
            return
    
    what = str(what)
    rtype = int(rtype)
    
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        
        try:
            await CallbackQuery.answer("Getting next results...")
            results = await YouTube.search(query, query_type)
        except:
            return await CallbackQuery.answer("Failed to get results.", show_alert=True)
        
        buttons = slider_markup(_, query_type, query, CallbackQuery.from_user.id)
        text = f"**Search Results for:** {query}\n\n"
        
        for i, result in enumerate(results):
            text += f"**{i+1}.** [{result['title'][:30]}...]({result['link']})\n"
            text += f"**Duration:** {result['duration']}\n\n"
        
        try:
            return await CallbackQuery.edit_message_text(
                text, reply_markup=InlineKeyboardMarkup(buttons)
            )
        except:
            return await CallbackQuery.answer("No more results available.", show_alert=True)
    
    if what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        
        try:
            await CallbackQuery.answer("Getting previous results...")
            results = await YouTube.search(query, query_type)
        except:
            return await CallbackQuery.answer("Failed to get results.", show_alert=True)
        
        buttons = slider_markup(_, query_type, query, CallbackQuery.from_user.id)
        text = f"**Search Results for:** {query}\n\n"
        
        for i, result in enumerate(results):
            text += f"**{i+1}.** [{result['title'][:30]}...]({result['link']})\n"
            text += f"**Duration:** {result['duration']}\n\n"
        
        try:
            return await CallbackQuery.edit_message_text(
                text, reply_markup=InlineKeyboardMarkup(buttons)
            )
        except:
            return await CallbackQuery.answer("No more results available.", show_alert=True)

@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
async def markup_panel(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = int(chat_id)
    
    buttons = panel_markup_1(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return

@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
async def del_back_playlist(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = int(chat_id)
    
    buttons = stream_markup(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return

@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
async def del_back_playlist(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("Bot is not active in voice chat.", show_alert=True)
    
    mention = CallbackQuery.from_user.mention
    
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer("Already paused.", show_alert=True)
        
        await music_on(chat_id)
        await Jhoom.pause_stream(chat_id)
        await CallbackQuery.answer("Music paused!")
        
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer("Already playing.", show_alert=True)
        
        await music_off(chat_id)
        await Jhoom.resume_stream(chat_id)
        await CallbackQuery.answer("Music resumed!")
        
    elif command == "Stop" or command == "End":
        await Jhoom.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.answer("Music stopped!")
        
    elif command == "Mute":
        await Jhoom.mute_stream(chat_id)
        await CallbackQuery.answer("Music muted!")
        
    elif command == "Unmute":
        await Jhoom.unmute_stream(chat_id)
        await CallbackQuery.answer("Music unmuted!")
        
    elif command == "Loop":
        await set_loop(chat_id, 1)
        await CallbackQuery.answer("Loop enabled!")
        
    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer("Empty queue.", show_alert=True)
        
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer("Empty queue.", show_alert=True)
        
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer("Queue has only one track.", show_alert=True)
        
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.answer("Queue shuffled!")
        
    elif command == "Skip":
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer("Empty queue.", show_alert=True)
        
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await Jhoom.stop_stream(chat_id)
                await set_loop(chat_id, 0)
                return await CallbackQuery.answer("Music stopped!")
            else:
                await Jhoom.skip_stream(chat_id, check[0]["file"])
        except:
            try:
                await Jhoom.stop_stream(chat_id)
                await set_loop(chat_id, 0)
            except:
                pass
            return await CallbackQuery.answer("Music stopped!")
        
        await CallbackQuery.answer("Music skipped!")

@app.on_callback_query(filters.regex("forceclose"))
async def force_close_callback(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid, chat_id = callback_request.split("|")
    
    if CallbackQuery.from_user.id != int(userid):
        try:
            return await CallbackQuery.answer(
                "This is not for you!",
                show_alert=True,
            )
        except:
            return
    
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex("close"))
async def close_callback(client, CallbackQuery: CallbackQuery):
    await CallbackQuery.message.delete()