# Stats inline keyboards (placeholder)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def stats_buttons():
    buttons = [
        [
            InlineKeyboardButton("📊 Bot Stats", callback_data="bot_stats"),
            InlineKeyboardButton("👥 User Stats", callback_data="user_stats")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back_to_start")
        ]
    ]
    return InlineKeyboardMarkup(buttons)