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
from JhoomMusic.platforms.youtube import YouTube
from JhoomMusic.plugins.tgcaller_handlers import jhoom_plugins
from config import BANNED_USERS

@app.on_message(
    filters.command(["play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def play_command(client, message: Message, _, chat_id):
    if len(message.command) < 2:
        return await message.reply_text("Please provide a song name or URL")
    
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
            "Anonymous Admin detected. Please use your personal account.", reply_markup=upl
        )
    
    if await is_music_playing(chat_id):
        await music_off(chat_id)
    
    query = message.text.split(None, 1)[1]
    mystic = await message.reply_text("🔍 Searching...")
    
    try:
        # Check if it's a YouTube URL
        if "youtube.com" in query or "youtu.be" in query:
            url = query
            if not await YouTube.exists(url, videoid=True):
                return await mystic.edit_text("Invalid YouTube URL")
            
            try:
                details, track_details = await YouTube.track(url, True)
            except Exception:
                return await mystic.edit_text("Failed to get track details")
        else:
            # Search for the query
            try:
                results = await YouTube.search(query)
            except:
                return await mystic.edit_text("Search failed")
            
            if not results:
                return await mystic.edit_text("No results found")
            
            # Use first result
            details = results[0]
            track_details = details
        
        streamtype = "video" if message.command[0][0] == "v" else "audio"
        
        if streamtype == "video":
            quality = "720"
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
            err = e if ex_type == "AssistantErr" else f"An error occurred: {ex_type}"
            return await mystic.edit_text(err)
        
        return await mystic.delete()

@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("Invalid command usage")
    
    if not await is_music_playing(chat_id):
        return await message.reply_text("Nothing is playing")
    
    await music_on(chat_id)
    await Jhoom.pause_stream(chat_id)
    await message.reply_text(
        f"⏸ Paused by {message.from_user.mention}"
    )

@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("Invalid command usage")
    
    if await is_music_playing(chat_id):
        return await message.reply_text("Already playing")
    
    await music_off(chat_id)
    await Jhoom.resume_stream(chat_id)
    await message.reply_text(
        f"▶️ Resumed by {message.from_user.mention}"
    )

@app.on_message(filters.command(["stop", "end", "cstop", "cend"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def stop_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("Invalid command usage")
    
    await Jhoom.stop_stream(chat_id)
    await message.reply_text(
        f"⏹ Stopped by {message.from_user.mention}"
    )

@app.on_message(filters.command(["skip", "cskip"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def skip_command(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("Invalid command usage")
    
    # Get next track from queue
    from JhoomMusic.utils.database.queue import get_queue, pop_an_item
    next_track = await get_queue(chat_id)
    
    if next_track:
        await pop_an_item(chat_id)
        await stream(
            _,
            message,
            next_track.get('user_id'),
            next_track,
            chat_id,
            next_track.get('user_name', 'Unknown'),
            chat_id,
            next_track.get('streamtype', 'audio'),
            next_track.get('quality', 'high')
        )
        await message.reply_text(
            f"⏭ Skipped by {message.from_user.mention}"
        )
    else:
        await Jhoom.stop_stream(chat_id)
        await message.reply_text(
            f"⏭ Skipped and stopped (no more tracks) by {message.from_user.mention}"
        )

@app.on_message(filters.command(["youtube", "yt"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def youtube_stream_command(client, message: Message, _, chat_id):
    """Stream YouTube using TgCaller plugin"""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a YouTube URL")
    
    url = message.text.split(None, 1)[1]
    mystic = await message.reply_text("🎵 Starting YouTube stream...")
    
    try:
        await jhoom_plugins.stream_youtube(chat_id, url, quality="high")
        await mystic.edit_text(f"🎵 YouTube stream started!\nURL: {url}")
    except Exception as e:
        await mystic.edit_text(f"❌ YouTube stream failed: {str(e)}")

@app.on_message(filters.command(["bridge"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def bridge_command(client, message: Message, _, chat_id):
    """Bridge two calls using TgCaller plugin"""
    if len(message.command) < 2:
        return await message.reply_text("Please provide target chat ID")
    
    try:
        target_chat_id = int(message.command[1])
        await jhoom_plugins.bridge_calls(chat_id, target_chat_id)
        await message.reply_text(f"🌉 Calls bridged: {chat_id} ↔ {target_chat_id}")
    except ValueError:
        await message.reply_text("❌ Invalid chat ID")
    except Exception as e:
        await message.reply_text(f"❌ Bridge failed: {str(e)}")