import asyncio
import os
import time
from pyrogram.types import InlineKeyboardMarkup
from JhoomMusic import YouTube, app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_assistant,
    get_audio_bitrate,
    get_lang,
    get_loop,
    get_video_bitrate,
    is_active_chat,
    is_video_allowed,
    music_off,
    remove_active_chat,
    remove_active_video_chat,
    set_loop
)
from JhoomMusic.utils.exceptions import AssistantErr
from JhoomMusic.utils.inline.play import stream_markup, telegram_markup
from JhoomMusic.utils.thumbnails import gen_thumb
from config import DURATION_LIMIT, SONG_DOWNLOAD_DURATION_LIMIT

async def stream(
    _,
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    streamtype,
    quality,
    forceplay: bool = None,
):
    if not result:
        return
    
    if forceplay:
        await Jhoom.stop_stream(chat_id)
    
    # Handle different result types
    if isinstance(result, dict):
        if "link" in result:
            link = result["link"]
            vidid = result.get("vidid", "unknown")
            title = result.get("title", "Unknown")
            duration_min = result.get("duration_min", "00:00")
            duration_sec = int(result.get("duration_sec", 0))
            thumbnail = result.get("thumb", "")
        else:
            # Handle search result format
            link = result.get("url", "")
            vidid = result.get("id", "unknown")
            title = result.get("title", "Unknown")
            duration_min = result.get("duration", "00:00")
            duration_sec = int(result.get("duration_seconds", 0))
            thumbnail = result.get("thumbnail", "")
    else:
        return await mystic.edit_text("Invalid result format")
    
    if duration_sec > DURATION_LIMIT:
        return await mystic.edit_text(
            f"Duration limit exceeded. Max: {DURATION_LIMIT//60} minutes"
        )
    
    try:
        await Jhoom.join_call(
            chat_id,
            original_chat_id,
            link,
            title,
            duration_min,
            user_name,
            vidid,
            streamtype,
            quality,
            forceplay,
        )
    except Exception as e:
        return await mystic.edit_text(f"Failed to join voice chat: {str(e)}")
    
    button = stream_markup(_, vidid, chat_id)
    
    try:
        img = await gen_thumb(vidid)
    except:
        img = "https://telegra.ph/file/c0e014ff34f34d1056627.png"
    
    await mystic.delete()
    
    caption = f"🎵 **Now Playing**\n\n"
    caption += f"**Title:** {title[:50]}...\n" if len(title) > 50 else f"**Title:** {title}\n"
    caption += f"**Duration:** {duration_min}\n"
    caption += f"**Requested by:** {user_name}"
    
    try:
        await app.send_photo(
            original_chat_id,
            photo=img,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(button),
        )
    except:
        await app.send_message(
            original_chat_id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(button),
        )
    
    if isinstance(img, str) and img.startswith("/"):
        try:
            os.remove(img)
        except:
            pass