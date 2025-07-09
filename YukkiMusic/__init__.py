import asyncio
import time
from motor.motor_asyncio import AsyncIOMotorClient

from pyrogram import Client
from pytgcalls import PyTgCalls

import config

from .logging import LOGGER

# Database
MONGO_DB_URI = config.MONGO_DB_URI
temp_client = AsyncIOMotorClient(MONGO_DB_URI)
db = temp_client.YukkiMusic

StartTime = time.time()

# Clients
app = Client(
    "YukkiBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

userbot = Client(
    "YukkiUserBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=str(config.STRING1),
)

pytgcalls = PyTgCalls(userbot)