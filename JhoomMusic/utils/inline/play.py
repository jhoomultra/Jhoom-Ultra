from pyrogram.types import InlineKeyboardButton
import config

def stream_markup(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
            InlineKeyboardButton(
                text="II", 
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="‣‣I", 
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▢", 
                callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀", 
                callback_data=f"ADMIN Shuffle|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔁", 
                callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎛 Panel", 
                callback_data=f"PanelMarkup {videoid}|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], 
                callback_data="close"
            )
        ],
    ]
    return buttons

def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
            InlineKeyboardButton(
                text="II", 
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="‣‣I", 
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▢", 
                callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀", 
                callback_data=f"ADMIN Shuffle|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔁", 
                callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], 
                callback_data="close"
            )
        ],
    ]
    return buttons

def close_markup(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], 
                callback_data="close"
            )
        ]
    ]
    return buttons

def livestream_markup(_, videoid, user_id, mode, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
            InlineKeyboardButton(
                text="II", 
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▢", 
                callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔁", 
                callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], 
                callback_data="close"
            )
        ],
    ]
    return buttons

def slider_markup(_, query_type, query, user_id):
    query = f"{query[:20]}..."
    buttons = [
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"Pages B|{query_type}|{query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▢",
                callback_data=f"forceclose {user_id}|{query_type}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"Pages F|{query_type}|{query}|{user_id}",
            ),
        ],
    ]
    return buttons

def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔇", 
                callback_data=f"ADMIN Mute|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔊", 
                callback_data=f"ADMIN Unmute|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀", 
                callback_data=f"ADMIN Shuffle|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔁", 
                callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁◁", 
                callback_data=f"ADMIN 1|{chat_id}"
            ),
            InlineKeyboardButton(
                text="◁", 
                callback_data=f"ADMIN 2|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▢", 
                callback_data=f"ADMIN Stop|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▷", 
                callback_data=f"ADMIN 3|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▷▷", 
                callback_data=f"ADMIN 4|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Back", 
                callback_data=f"MainMarkup {videoid}|{chat_id}"
            ),
        ],
    ]
    return buttons

def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Audio", 
                callback_data=f"ADMIN Audio|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🎬 Video", 
                callback_data=f"ADMIN Video|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Back", 
                callback_data=f"MainMarkup {videoid}|{chat_id}"
            ),
        ],
    ]
    return buttons

def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔊 Low", 
                callback_data=f"ADMIN LowVolume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔉 Medium", 
                callback_data=f"ADMIN MediumVolume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔊 High", 
                callback_data=f"ADMIN HighVolume|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Back", 
                callback_data=f"MainMarkup {videoid}|{chat_id}"
            ),
        ],
    ]
    return buttons