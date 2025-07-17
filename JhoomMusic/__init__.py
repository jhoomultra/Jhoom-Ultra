import time
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from tgcaller import TgCaller
from tgcaller.types import MediaStream
from tgcaller.types.input_stream import AudioPiped, AudioVideoPiped
from tgcaller.types.input_stream.quality import HighQualityAudio, HighQualityVideo

import config
from JhoomMusic.logging import LOGGER

# Database
MONGO_DB_URI = config.MONGO_DB_URI
temp_client = AsyncIOMotorClient(MONGO_DB_URI)
db = temp_client.JhoomMusic

StartTime = time.time()

# Clients
app = Client(
    "JhoomBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

userbot = Client(
    "JhoomUserBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=str(config.STRING1),
) if config.STRING1 else None

# TgCaller - Updated initialization
tgcaller = TgCaller(userbot if userbot else app)

# YouTube
from JhoomMusic.platforms.youtube import YouTube