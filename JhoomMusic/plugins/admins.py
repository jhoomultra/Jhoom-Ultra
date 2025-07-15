import asyncio
from pyrogram import filters
from pyrogram.types import Message
from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import (
    get_assistant, 
    get_authuser_names, 
    get_cmode, 
    is_active_chat,
    is_commanddelete_on,
    is_maintenance
)
from JhoomMusic.utils.decorators import AdminRightsCheck, language
from JhoomMusic.utils.inline.settings import admin_markup
from config import BANNED_USERS

@app.on_message(
    filters.command(["reload", "refresh"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def reload_admin_cache(client, message: Message, _, chat_id):
    try:
        if await is_maintenance() is False:
            return await message.reply_text(
                "Bot is under maintenance. Please try again later."
            )
        
        admins = await app.get_chat_administrators(chat_id)
        authusers = await get_authuser_names(chat_id)
        adminlist = []
        
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist.append(user.user.id)
        
        for user in authusers:
            adminlist.append(user)
        
        adminlist.append(1087968824)  # Anonymous Admin
        
        try:
            adminlist.remove(app.id)
        except:
            pass
        
        adminlist = list(set(adminlist))
        
        await message.reply_text(
            _["admin_20"].format(len(adminlist))
        )
        
    except Exception as e:
        await message.reply_text(f"Failed to reload admin cache: {e}")

@app.on_message(
    filters.command(["reboot"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def restart_bot(client, message: Message, _, chat_id):
    mystic = await message.reply_text(
        f"**{app.mention} is restarting...**\n\nPlease wait for a few seconds!"
    )
    
    await asyncio.sleep(1)
    await mystic.edit_text(
        "**Restarted Successfully**\n\nNow you can use the bot!"
    )
    
    try:
        await Jhoom.stop_stream_force(chat_id)
    except:
        pass

@app.on_message(
    filters.command(["maintenance"]) & filters.user(config.OWNER_ID)
)
async def maintenance_mode(client, message: Message):
    try:
        if await is_maintenance():
            await maintenance_off()
            await message.reply_text(
                "**Maintenance Mode Disabled**\n\nBot is now available for all users."
            )
        else:
            await maintenance_on()
            await message.reply_text(
                "**Maintenance Mode Enabled**\n\nBot is now under maintenance."
            )
    except Exception as e:
        await message.reply_text(f"Failed to toggle maintenance mode: {e}")

@app.on_message(
    filters.command(["logger"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def logger_command(client, message: Message, _, chat_id):
    if await is_commanddelete_on(chat_id):
        await commanddelete_off(chat_id)
        await message.reply_text("**Command Delete Disabled**")
    else:
        await commanddelete_on(chat_id)
        await message.reply_text("**Command Delete Enabled**")

@app.on_message(
    filters.command(["assistant", "asst"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def assistant_command(client, message: Message, _, chat_id):
    if len(message.command) != 2:
        return await message.reply_text("**Usage:** /assistant [1-5]")
    
    try:
        query = int(message.command[1])
    except:
        return await message.reply_text("**Usage:** /assistant [1-5]")
    
    if query > 5 or query < 1:
        return await message.reply_text("**Usage:** /assistant [1-5]")
    
    await save_assistant(chat_id, query)
    await message.reply_text(f"**Assistant changed to:** Assistant {query}")

@app.on_message(
    filters.command(["activevc", "activevoice"]) & filters.group & ~BANNED_USERS
)
async def activevc_command(client, message: Message):
    mystic = await message.reply_text("Getting active voice chats...")
    
    served_chats = []
    try:
        async for chat in get_active_chats():
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await mystic.edit_text(f"**Error:** {e}")
        return
    
    text = "**Active Voice Chats:**\n\n"
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except:
            title = "Private Group"
        
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"**{j + 1}.** [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    
    if not served_chats:
        text = "**No Active Voice Chats**"
    
    await mystic.edit_text(text)

@app.on_message(
    filters.command(["activevideo"]) & filters.group & ~BANNED_USERS
)
async def activevideo_command(client, message: Message):
    mystic = await message.reply_text("Getting active video chats...")
    
    served_chats = []
    try:
        async for chat in get_active_video_chats():
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await mystic.edit_text(f"**Error:** {e}")
        return
    
    text = "**Active Video Chats:**\n\n"
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except:
            title = "Private Group"
        
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"**{j + 1}.** [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    
    if not served_chats:
        text = "**No Active Video Chats**"
    
    await mystic.edit_text(text)