from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from YukkiMusic import app
from YukkiMusic.utils.database import add_served_chat, add_served_user
from config import BANNED_USERS


@app.on_message(filters.command("start") & ~BANNED_USERS)
async def start_command(client, message: Message):
    await add_served_chat(message.chat.id)
    await add_served_user(message.from_user.id)
    
    await message.reply_text(
        f"🎵 **Welcome to Yukki Music Bot!**\n\n"
        f"I can play music in your group's voice chat.\n\n"
        f"**Commands:**\n"
        f"• `/play` - Play a song\n"
        f"• `/pause` - Pause current song\n"
        f"• `/resume` - Resume paused song\n"
        f"• `/skip` - Skip current song\n"
        f"• `/stop` - Stop playing and clear queue\n\n"
        f"Add me to your group and make me admin with voice chat permissions!",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Commands", callback_data="settings_back_helper"
                    ),
                    InlineKeyboardButton(
                        "⚙️ Settings", callback_data="settings_helper"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📨 Support Group", url="https://t.me/YukkiSupport"
                    ),
                    InlineKeyboardButton(
                        "📢 Updates Channel", url="https://t.me/TeamYukki"
                    ),
                ],
            ]
        ),
    )


@app.on_message(filters.command("help") & ~BANNED_USERS)
async def help_command(client, message: Message):
    await message.reply_text(
        "🎵 **Yukki Music Bot Help**\n\n"
        "**Basic Commands:**\n"
        "• `/play [song name]` - Play a song from YouTube\n"
        "• `/play [reply to audio]` - Play replied audio file\n"
        "• `/pause` - Pause the current song\n"
        "• `/resume` - Resume the paused song\n"
        "• `/skip` - Skip to next song in queue\n"
        "• `/stop` - Stop playing and clear queue\n"
        "• `/queue` - Show current queue\n"
        "• `/shuffle` - Shuffle the queue\n\n"
        "**Admin Commands:**\n"
        "• `/reload` - Reload admin cache\n"
        "• `/maintenance [on/off]` - Enable/disable maintenance mode\n\n"
        "**Note:** Add the bot to your group and give admin permissions with voice chat access."
    )