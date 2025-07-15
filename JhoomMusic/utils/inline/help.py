from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def help_pannel(_, START: Union[bool, int] = None):
    first = [
        InlineKeyboardButton(
            text="🎵 Basic Commands",
            callback_data="help_callback hb1"
        ),
        InlineKeyboardButton(
            text="🎛️ Admin Commands", 
            callback_data="help_callback hb2"
        ),
    ]
    second = [
        InlineKeyboardButton(
            text="🔧 Settings",
            callback_data="help_callback hb3"
        ),
        InlineKeyboardButton(
            text="📊 Statistics", 
            callback_data="help_callback hb4"
        ),
    ]
    third = [
        InlineKeyboardButton(
            text="🎭 Playlist",
            callback_data="help_callback hb5"
        ),
        InlineKeyboardButton(
            text="🎪 Extras", 
            callback_data="help_callback hb6"
        ),
    ]
    fourth = [
        InlineKeyboardButton(
            text="🔙 Back",
            callback_data="settingsback_helper"
        ),
        InlineKeyboardButton(
            text="🗂 Support",
            url=config.SUPPORT_GROUP
        ),
    ]
    return [first, second, third, fourth]

def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="settings_back_helper",
                ),
                InlineKeyboardButton(
                    text="🔄 Close", callback_data="close"
                )
            ]
        ]
    )
    return upl

def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Basic Commands",
                callback_data="help_callback hb1"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎛️ Admin Commands", 
                callback_data="help_callback hb2"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔧 Settings",
                callback_data="help_callback hb3"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📊 Statistics", 
                callback_data="help_callback hb4"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎭 Playlist",
                callback_data="help_callback hb5"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎪 Extras", 
                callback_data="help_callback hb6"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗂 Support Group", url=config.SUPPORT_GROUP
            ),
            InlineKeyboardButton(
                text="📢 Updates Channel", url=config.SUPPORT_CHANNEL
            ),
        ],
    ]
    return buttons
