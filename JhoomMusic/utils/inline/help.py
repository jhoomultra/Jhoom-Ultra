from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

def help_pannel(_, START: Union[bool, int] = None):
    first = [
        InlineKeyboardButton(
            text=_["HELP_1"],
            callback_data="help_callback hb1"
        ),
        InlineKeyboardButton(
            text=_["HELP_2"], 
            callback_data="help_callback hb2"
        ),
    ]
    second = [
        InlineKeyboardButton(
            text=_["HELP_3"],
            callback_data="help_callback hb3"
        ),
        InlineKeyboardButton(
            text=_["HELP_4"], 
            callback_data="help_callback hb4"
        ),
    ]
    third = [
        InlineKeyboardButton(
            text=_["HELP_5"],
            callback_data="help_callback hb5"
        ),
        InlineKeyboardButton(
            text=_["HELP_6"], 
            callback_data="help_callback hb6"
        ),
    ]
    fourth = [
        InlineKeyboardButton(
            text=_["HELP_7"],
            callback_data="help_callback hb7"
        ),
        InlineKeyboardButton(
            text=_["HELP_8"], 
            callback_data="help_callback hb8"
        ),
    ]
    fifth = [
        InlineKeyboardButton(
            text=_["HELP_9"],
            callback_data="help_callback hb9"
        ),
        InlineKeyboardButton(
            text=_["HELP_10"], 
            callback_data="help_callback hb10"
        ),
    ]
    sixth = [
        InlineKeyboardButton(
            text=_["HELP_11"],
            callback_data="help_callback hb11"
        ),
        InlineKeyboardButton(
            text=_["HELP_12"], 
            callback_data="help_callback hb12"
        ),
    ]
    seventh = [
        InlineKeyboardButton(
            text=_["HELP_13"],
            callback_data="help_callback hb13"
        ),
        InlineKeyboardButton(
            text=_["HELP_14"], 
            callback_data="help_callback hb14"
        ),
    ]
    eighth = [
        InlineKeyboardButton(
            text=_["HELP_15"],
            callback_data="help_callback hb15"
        ),
    ]
    
    if START:
        ninth = [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"settingsback_helper"
            ),
            InlineKeyboardButton(
                text=_["SUPPORT_BUTTON"], 
                url=config.SUPPORT_GROUP
            ),
        ]
    else:
        ninth = [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"settings_back_helper"
            ),
            InlineKeyboardButton(
                text=_["SUPPORT_BUTTON"], 
                url=config.SUPPORT_GROUP
            ),
        ]
    
    return [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth]

def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"], 
                    callback_data=f"close"
                )
            ]
        ]
    )
    return upl

def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["HELP_1"],
                callback_data="help_callback hb1"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_2"], 
                callback_data="help_callback hb2"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_3"],
                callback_data="help_callback hb3"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_4"], 
                callback_data="help_callback hb4"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_5"],
                callback_data="help_callback hb5"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_6"], 
                callback_data="help_callback hb6"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_7"],
                callback_data="help_callback hb7"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_8"], 
                callback_data="help_callback hb8"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_9"],
                callback_data="help_callback hb9"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_10"], 
                callback_data="help_callback hb10"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_11"],
                callback_data="help_callback hb11"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_12"], 
                callback_data="help_callback hb12"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_13"],
                callback_data="help_callback hb13"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_14"], 
                callback_data="help_callback hb14"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["HELP_15"],
                callback_data="help_callback hb15"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["SUPPORT_BUTTON"], 
                url=config.SUPPORT_GROUP
            ),
            InlineKeyboardButton(
                text=_["SUPPORT_CHANNEL"], 
                url=config.SUPPORT_CHANNEL
            ),
        ],
    ]
    return buttons