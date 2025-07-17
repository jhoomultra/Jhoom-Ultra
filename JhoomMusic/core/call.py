import asyncio
from typing import Dict, Union, Optional
from tgcaller import TgCaller
from tgcaller.types import Update
from tgcaller.types.input_stream import AudioPiped, AudioVideoPiped
from tgcaller.types.input_stream.quality import (
    HighQualityAudio, 
    HighQualityVideo, 
    MediumQualityAudio, 
    MediumQualityVideo
)
from tgcaller.exceptions import NoActiveGroupCall, GroupCallNotFound

import config
from JhoomMusic import LOGGER, app, userbot, tgcaller
from JhoomMusic.utils.database import add_active_chat, remove_active_chat

class JhoomCall:
    def __init__(self):
        self.tgcaller = tgcaller
        self.active_calls = {}

    async def start(self):
        """Start TgCaller"""
        try:
            await self.tgcaller.start()
            LOGGER(__name__).info("TgCaller started successfully")
        except Exception as e:
            LOGGER(__name__).error(f"Failed to start TgCaller: {e}")
            raise e

    async def pause_stream(self, chat_id: int):
        """Pause stream in a chat"""
        try:
            await self.tgcaller.pause_stream(chat_id)
            LOGGER(__name__).info(f"Stream paused in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error pausing stream in {chat_id}: {e}")
            raise e

    async def resume_stream(self, chat_id: int):
        """Resume stream in a chat"""
        try:
            await self.tgcaller.resume_stream(chat_id)
            LOGGER(__name__).info(f"Stream resumed in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error resuming stream in {chat_id}: {e}")
            raise e

    async def stop_stream(self, chat_id: int):
        """Stop stream and leave call"""
        try:
            await self.tgcaller.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            if chat_id in self.active_calls:
                del self.active_calls[chat_id]
            LOGGER(__name__).info(f"Stream stopped in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping stream in {chat_id}: {e}")
            raise e

    async def skip_stream(self, chat_id: int, link: str, video: bool = False):
        """Skip to next track"""
        try:
            if video:
                stream = AudioVideoPiped(
                    link,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=HighQualityVideo()
                )
            else:
                stream = AudioPiped(link, audio_parameters=HighQualityAudio())
            
            await self.tgcaller.change_stream(chat_id, stream)
            LOGGER(__name__).info(f"Stream skipped in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error skipping stream in {chat_id}: {e}")
            raise e

    async def mute_stream(self, chat_id: int):
        """Mute stream"""
        try:
            await self.tgcaller.mute_stream(chat_id)
            LOGGER(__name__).info(f"Stream muted in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error muting stream in {chat_id}: {e}")
            raise e

    async def unmute_stream(self, chat_id: int):
        """Unmute stream"""
        try:
            await self.tgcaller.unmute_stream(chat_id)
            LOGGER(__name__).info(f"Stream unmuted in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error unmuting stream in {chat_id}: {e}")
            raise e

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
        """Join group call and start streaming"""
        try:
            # Choose quality based on parameter
            if quality == "high":
                audio_quality = HighQualityAudio()
                video_quality = HighQualityVideo()
            else:
                audio_quality = MediumQualityAudio()
                video_quality = MediumQualityVideo()
            
            # Create stream based on type
            if streamtype == "video":
                stream = AudioVideoPiped(
                    link,
                    audio_parameters=audio_quality,
                    video_parameters=video_quality
                )
            else:
                stream = AudioPiped(link, audio_parameters=audio_quality)
            
            # Join the call
            await self.tgcaller.join_group_call(chat_id, stream)
            await add_active_chat(chat_id)
            
            # Store call info
            self.active_calls[chat_id] = {
                'title': title,
                'duration': duration,
                'user_name': user_name,
                'videoid': videoid,
                'streamtype': streamtype,
                'quality': quality
            }
            
            LOGGER(__name__).info(f"Successfully joined call in {chat_id}")
            
        except NoActiveGroupCall:
            LOGGER(__name__).error(f"No active voice chat found in {chat_id}")
            raise Exception("No active voice chat found")
        except GroupCallNotFound:
            LOGGER(__name__).error(f"Group call not found in {chat_id}")
            raise Exception("Group call not found")
        except Exception as e:
            LOGGER(__name__).error(f"Error joining call in {chat_id}: {e}")
            raise e

    async def stream_call(self, link: str):
        """Test stream call"""
        try:
            # This is for initial stream test
            LOGGER(__name__).info(f"Testing stream with link: {link}")
        except Exception as e:
            LOGGER(__name__).error(f"Stream call error: {e}")
            raise e

    async def decorators(self):
        """Setup event decorators"""
        @self.tgcaller.on_stream_end()
        async def on_stream_end(client: TgCaller, update: Update):
            chat_id = update.chat_id
            await remove_active_chat(chat_id)
            if chat_id in self.active_calls:
                del self.active_calls[chat_id]
            LOGGER(__name__).info(f"Stream ended in {chat_id}")

        @self.tgcaller.on_closed_voice_chat()
        async def on_closed_voice_chat(client: TgCaller, update: Update):
            chat_id = update.chat_id
            await remove_active_chat(chat_id)
            if chat_id in self.active_calls:
                del self.active_calls[chat_id]
            LOGGER(__name__).info(f"Voice chat closed in {chat_id}")

    async def stop_stream_force(self, chat_id: int):
        """Force stop stream"""
        try:
            await self.tgcaller.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            if chat_id in self.active_calls:
                del self.active_calls[chat_id]
            LOGGER(__name__).info(f"Stream force stopped in {chat_id}")
        except Exception as e:
            LOGGER(__name__).error(f"Error force stopping stream in {chat_id}: {e}")
            raise e

    async def get_call_info(self, chat_id: int) -> Optional[Dict]:
        """Get call information"""
        return self.active_calls.get(chat_id)

    async def is_connected(self, chat_id: int) -> bool:
        """Check if connected to call"""
        return chat_id in self.active_calls

# Global instance
Jhoom = JhoomCall()