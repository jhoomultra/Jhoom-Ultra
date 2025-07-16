import asyncio
from typing import Dict, Union
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from pytgcalls.exceptions import NoActiveGroupCall

import config
from JhoomMusic import LOGGER, app, userbot, pytgcalls
from JhoomMusic.utils.database import add_active_chat, remove_active_chat

class Call:
    def __init__(self):
        self.pytgcalls = pytgcalls

    async def pause_stream(self, chat_id: int):
        try:
            await self.pytgcalls.pause_stream(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error pausing stream in {chat_id}: {e}")

    async def resume_stream(self, chat_id: int):
        try:
            await self.pytgcalls.resume_stream(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error resuming stream in {chat_id}: {e}")

    async def stop_stream(self, chat_id: int):
        try:
            await self.pytgcalls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping stream in {chat_id}: {e}")

    async def skip_stream(self, chat_id: int, link: str, video: bool = False):
        try:
            if video:
                stream = AudioVideoPiped(
                    link,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=HighQualityVideo()
                )
            else:
                stream = AudioPiped(link, audio_parameters=HighQualityAudio())
            
            await self.pytgcalls.change_stream(chat_id, stream)
        except Exception as e:
            LOGGER(__name__).error(f"Error skipping stream in {chat_id}: {e}")

    async def mute_stream(self, chat_id: int):
        try:
            await self.pytgcalls.mute_stream(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error muting stream in {chat_id}: {e}")

    async def unmute_stream(self, chat_id: int):
        try:
            await self.pytgcalls.unmute_stream(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error unmuting stream in {chat_id}: {e}")

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link: str,
        title: str,
        duration: str,
        user_name: str,
        videoid: str,
        streamtype: str,
        quality: str,
        forceplay: bool = False
    ):
        try:
            if streamtype == "video":
                stream = AudioVideoPiped(
                    link,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=HighQualityVideo()
                )
            else:
                stream = AudioPiped(link, audio_parameters=HighQualityAudio())
            
            await self.pytgcalls.join_group_call(chat_id, stream)
            await add_active_chat(chat_id)
            
        except NoActiveGroupCall:
            raise Exception("No active voice chat found")
        except Exception as e:
            LOGGER(__name__).error(f"Error joining call in {chat_id}: {e}")
            raise e

    async def stream_call(self, link: str):
        try:
            # This is for initial stream test
            pass
        except Exception as e:
            LOGGER(__name__).error(f"Stream call error: {e}")

    async def decorators(self):
        # Setup decorators and handlers
        @self.pytgcalls.on_stream_end()
        async def on_stream_end(client: PyTgCalls, update: Update):
            chat_id = update.chat_id
            await remove_active_chat(chat_id)

    async def start(self):
        await self.pytgcalls.start()
        LOGGER(__name__).info("PyTgCalls started successfully")

Jhoom = Call()