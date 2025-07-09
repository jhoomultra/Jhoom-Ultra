import asyncio
from typing import Union

from pyrogram import Client
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)

import config
from YukkiMusic import LOGGER, app, userbot

from ..utils.database import add_active_chat, remove_active_chat


class Call:
    def __init__(self):
        self.pytgcalls = PyTgCalls(userbot, cache_duration=100)

    async def pause_stream(self, chat_id: int):
        try:
            await self.pytgcalls.pause_stream(chat_id)
        except:
            pass

    async def resume_stream(self, chat_id: int):
        try:
            await self.pytgcalls.resume_stream(chat_id)
        except:
            pass

    async def stop_stream(self, chat_id: int):
        try:
            await self.pytgcalls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
        except:
            pass

    async def force_stop_stream(self, chat_id: int):
        try:
            await self.pytgcalls.leave_group_call(chat_id)
        except:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        if video:
            stream = AudioVideoPiped(
                link,
                HighQualityAudio(),
                HighQualityVideo(),
            )
        else:
            stream = AudioPiped(link, HighQualityAudio())
        try:
            await self.pytgcalls.change_stream(
                chat_id,
                stream,
            )
        except Exception as e:
            LOGGER(__name__).error(f"Error in skip_stream: {e}")
            return False
        return True

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        stream = (
            AudioVideoPiped(
                file_path,
                HighQualityAudio(),
                HighQualityVideo(),
            )
            if mode == "video"
            else AudioPiped(file_path, HighQualityAudio())
        )
        try:
            await self.pytgcalls.change_stream(chat_id, stream)
        except Exception as e:
            LOGGER(__name__).error(f"Error in seek_stream: {e}")
            return False
        return True

    async def stream_call(self, link, video: Union[bool, str] = None):
        if video:
            stream = AudioVideoPiped(
                link,
                HighQualityAudio(),
                HighQualityVideo(),
            )
        else:
            stream = AudioPiped(link, HighQualityAudio())
        try:
            await self.pytgcalls.join_group_call(
                config.LOG_GROUP_ID,
                stream,
            )
        except Exception as e:
            LOGGER(__name__).error(f"Error in stream_call: {e}")
            return False
        return True

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        if video:
            stream = AudioVideoPiped(
                link,
                HighQualityAudio(),
                HighQualityVideo(),
            )
        else:
            stream = AudioPiped(link, HighQualityAudio())
        try:
            await self.pytgcalls.join_group_call(
                chat_id,
                stream,
            )
            await add_active_chat(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error in join_call: {e}")
            return False
        return True

    async def change_stream(self, client, chat_id):
        try:
            await self.pytgcalls.change_stream(
                chat_id,
                AudioPiped("https://telegra.ph/file/29f784eb49d230ab62e9e.mp4"),
            )
        except:
            pass

    async def start(self):
        await self.pytgcalls.start()

    async def decorators(self):
        @self.pytgcalls.on_kicked()
        async def on_kicked(_, chat_id: int):
            try:
                await remove_active_chat(chat_id)
            except:
                pass

        @self.pytgcalls.on_closed_voice_chat()
        async def on_closed_voice_chat(_, chat_id: int):
            try:
                await remove_active_chat(chat_id)
            except:
                pass

        @self.pytgcalls.on_left()
        async def on_left(_, chat_id: int):
            try:
                await remove_active_chat(chat_id)
            except:
                pass


Yukki = Call()