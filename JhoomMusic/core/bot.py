import asyncio
import importlib
import sys
from pyrogram import idle
from tgcaller.exceptions import NoActiveGroupCall

import config
from JhoomMusic import LOGGER, app, userbot
from JhoomMusic.core.call import Jhoom
from JhoomMusic.misc import sudo
from JhoomMusic.plugins import ALL_MODULES
from JhoomMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    
    await sudo()
    
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    
    await app.start()
    
    for all_module in ALL_MODULES:
        importlib.import_module("JhoomMusic.plugins." + all_module)
    
    LOGGER("JhoomMusic.plugins").info("Successfully Imported Modules...")
    
    if userbot:
        await userbot.start()
    
    await Jhoom.start()
    
    try:
        await Jhoom.stream_call("https://telegra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("JhoomMusic").error(
            "Please turn on the videochat of your log group\\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    
    await Jhoom.decorators()
    LOGGER("JhoomMusic").info(
        "Jhoom Music Bot Started Successfully, Now go and play some music!"
    )
    
    await idle()
    await app.stop()
    if userbot:
        await userbot.stop()
    LOGGER("JhoomMusic").info("Stopping Jhoom Music Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())