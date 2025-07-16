# Settings inline keyboards (placeholder)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_markup():
    buttons = [
        [
            InlineKeyboardButton("🔊 Audio Quality", callback_data="audio_quality"),
            InlineKeyboardButton("🎬 Video Quality", callback_data="video_quality")
        ],
        [
            InlineKeyboardButton("🔄 Auto Leave", callback_data="auto_leave"),
            InlineKeyboardButton("🧹 Clean Mode", callback_data="clean_mode")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back_to_start")
        ]
    ]
    return InlineKeyboardMarkup(buttons)