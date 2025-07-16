# Playlist inline keyboards (placeholder)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def playlist_buttons():
    buttons = [
        [
            InlineKeyboardButton("➕ Create Playlist", callback_data="create_playlist"),
            InlineKeyboardButton("📋 My Playlists", callback_data="my_playlists")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back_to_start")
        ]
    ]
    return InlineKeyboardMarkup(buttons)