from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from JhoomMusic.utils.database import add_served_chat, add_served_user
from config import BANNED_USERS

@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
async def start_private(client, message: Message):
    await add_served_user(message.from_user.id)
    
    await message.reply_text(
        f"🎵 **Welcome to Jhoom Music Bot!**\n\n"
        f"I can play music in your group's voice chat.\n\n"
        f"**Commands:**\n"
        f"• /play - Play music\n"
        f"• /pause - Pause music\n"
        f"• /resume - Resume music\n"
        f"• /skip - Skip current track\n"
        f"• /stop - Stop music\n\n"
        f"Add me to your group and enjoy music!",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add to Group", url=f"https://t.me/{app.me.username}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📨 Support Group", url="https://t.me/JhoomSupport"
                    ),
                    InlineKeyboardButton(
                        "📢 Updates Channel", url="https://t.me/TeamJhoom"
                    ),
                ],
            ]
        ),
    )

@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
async def start_group(client, message: Message):
    await add_served_chat(message.chat.id)
    
    await message.reply_text(
        f"🎵 **Jhoom Music Bot is ready!**\n\n"
        f"Use /play [song name] to start playing music."
    )

@app.on_message(filters.command("help") & ~BANNED_USERS)
async def help_command(client, message: Message):
    await message.reply_text(
        "🎵 **Jhoom Music Bot Help**\n\n"
        "**Basic Commands:**\n"
        "• /play [song] - Play music\n"
        "• /pause - Pause current track\n"
        "• /resume - Resume paused track\n"
        "• /skip - Skip to next track\n"
        "• /stop - Stop music and clear queue\n"
        "• /queue - Show current queue\n\n"
        "**Admin Commands:**\n"
        "• /auth [user_id] - Authorize user\n"
        "• /unauth [user_id] - Remove authorization\n"
        "• /reload - Reload admin cache\n\n"
        "**Settings:**\n"
        "• /settings - Open settings panel"
    )