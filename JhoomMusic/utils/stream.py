import asyncio
import os
import time
from pyrogram.types import InlineKeyboardMarkup
from JhoomMusic import YouTube, app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    db,
    get_assistant,
    get_audio_bitrate,
    get_lang,
    get_loop,
    get_video_bitrate,
    group_db,
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
    
    if streamtype == "playlist":
        msg = f"{_['playlist_16']}\n\n"
        count = 0
        for search in result:
            if int(count) == PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                    videoid,
                ) = search
                if str(duration_min) == "None":
                    continue
                if duration_sec > DURATION_LIMIT:
                    continue
                if await is_active_chat(chat_id):
                    await put_queue(
                        chat_id,
                        original_chat_id,
                        f"vid_{videoid}",
                        title,
                        duration_min,
                        user_name,
                        videoid,
                        user_id,
                        "video" if streamtype == "video" else "audio",
                    )
                    position = len(db.get(chat_id)) - 1
                    count += 1
                    msg += f"{count}- {title[:70]}\n"
                    msg += f"{_['playlist_17']} {position}\n\n"
                else:
                    await Jhoom.join_call(
                        chat_id,
                        original_chat_id,
                        f"vid_{videoid}",
                        title,
                        duration_min,
                        user_name,
                        videoid,
                        streamtype,
                        quality,
                        forceplay,
                    )
                    count += 1
                    msg += f"{count}- {title[:70]}\n"
            except Exception:
                continue
        
        if count == 0:
            return
        else:
            if forceplay:
                await mystic.edit_text(msg)
            else:
                buttons = telegram_markup(_, chat_id)
                await mystic.edit_text(
                    msg, reply_markup=InlineKeyboardMarkup(buttons)
                )
    
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = result["title"]
        duration_min = result["duration_min"]
        duration_sec = int(result["duration_sec"])
        thumbnail = result["thumb"]
        
        if duration_sec > DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(DURATION_LIMIT_MIN, duration_min)
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
            return await mystic.edit_text(_["call_7"])
        
        button = stream_markup(_, vidid, chat_id)
        img = await gen_thumb(vidid)
        await mystic.delete()
        
        await app.send_photo(
            original_chat_id,
            photo=img,
            caption=_["stream_1"].format(
                title[:27],
                f"https://t.me/{app.username}?start=info_{vidid}",
                duration_min,
                user_name,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        
        os.remove(img)
    
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        duration_sec = int(result["duration_sec"])
        thumbnail = result["thumb"]
        
        if duration_sec > DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(DURATION_LIMIT_MIN, duration_min)
            )
        
        try:
            await Jhoom.join_call(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                thumbnail,
                streamtype,
                quality,
                forceplay,
            )
        except Exception as e:
            return await mystic.edit_text(_["call_7"])
        
        button = telegram_markup(_, chat_id)
        await mystic.edit_text(
            _["stream_3"].format(title, duration_min, user_name),
            reply_markup=InlineKeyboardMarkup(button),
        )
    
    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = result["title"]
        duration_min = result["duration_min"]
        duration_sec = int(result["duration_sec"])
        
        if duration_sec > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_7"].format(SONG_DOWNLOAD_DURATION_LIMIT_MIN, duration_min)
            )
        
        try:
            await Jhoom.join_call(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                link,
                streamtype,
                quality,
                forceplay,
            )
        except Exception as e:
            return await mystic.edit_text(_["call_7"])
        
        button = telegram_markup(_, chat_id)
        await mystic.edit_text(
            _["stream_4"].format(title, duration_min),
            reply_markup=InlineKeyboardMarkup(button),
        )
    
    elif streamtype == "live":
        link = result["link"]
        title = result["title"]
        thumbnail = result["thumb"]
        duration_min = "Live Stream"
        
        try:
            await Jhoom.join_call(
                chat_id,
                original_chat_id,
                link,
                title,
                duration_min,
                user_name,
                thumbnail,
                streamtype,
                quality,
                forceplay,
            )
        except Exception as e:
            return await mystic.edit_text(_["call_7"])
        
        button = telegram_markup(_, chat_id)
        await mystic.edit_text(
            _["stream_2"].format(user_name),
            reply_markup=InlineKeyboardMarkup(button),
        )
    
    elif streamtype == "index":
        link = result
        title = "Index or M3u8 Link"
        duration_min = "URL stream"
        
        try:
            await Jhoom.join_call(
                chat_id,
                original_chat_id,
                link,
                title,
                duration_min,
                user_name,
                link,
                streamtype,
                quality,
                forceplay,
            )
        except Exception as e:
            return await mystic.edit_text(_["call_7"])
        
        button = telegram_markup(_, chat_id)
        await mystic.edit_text(
            _["stream_2"].format(user_name),
            reply_markup=InlineKeyboardMarkup(button),
        )