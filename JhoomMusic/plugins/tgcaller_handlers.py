"""
TgCaller Event Handlers and Plugins
"""
import asyncio
from typing import Dict, Any
from tgcaller import TgCaller
from tgcaller.types import Update
from tgcaller.plugins import YouTubeStreamer, BridgedCallManager

from JhoomMusic import LOGGER, tgcaller
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import remove_active_chat

class JhoomTgCallerPlugins:
    def __init__(self):
        self.youtube_streamer = None
        self.bridge_manager = None
        self.setup_plugins()

    def setup_plugins(self):
        """Setup TgCaller plugins"""
        try:
            # YouTube Streamer Plugin
            self.youtube_streamer = YouTubeStreamer()
            
            # Bridged Call Manager Plugin
            self.bridge_manager = BridgedCallManager()
            
            LOGGER(__name__).info("TgCaller plugins initialized")
        except Exception as e:
            LOGGER(__name__).error(f"Error setting up plugins: {e}")

    async def stream_youtube(self, chat_id: int, url: str, quality: str = "high"):
        """Stream YouTube video using plugin"""
        try:
            if self.youtube_streamer:
                await self.youtube_streamer.stream(chat_id, url, quality)
                LOGGER(__name__).info(f"YouTube streaming started in {chat_id}")
            else:
                raise Exception("YouTube streamer plugin not available")
        except Exception as e:
            LOGGER(__name__).error(f"YouTube streaming error: {e}")
            raise e

    async def bridge_calls(self, chat_id1: int, chat_id2: int):
        """Bridge two calls"""
        try:
            if self.bridge_manager:
                await self.bridge_manager.bridge(chat_id1, chat_id2)
                LOGGER(__name__).info(f"Calls bridged: {chat_id1} <-> {chat_id2}")
            else:
                raise Exception("Bridge manager plugin not available")
        except Exception as e:
            LOGGER(__name__).error(f"Call bridging error: {e}")
            raise e

# Event Handlers
@tgcaller.on_stream_end()
async def on_stream_end_handler(client: TgCaller, update: Update):
    """Handle stream end event"""
    chat_id = update.chat_id
    try:
        await remove_active_chat(chat_id)
        LOGGER(__name__).info(f"Stream ended in chat {chat_id}")
        
        # Auto-play next track if queue exists
        from JhoomMusic.utils.database.queue import get_queue
        next_track = await get_queue(chat_id)
        if next_track:
            from JhoomMusic.utils.stream import stream
            await stream(
                None,  # language
                None,  # mystic message
                next_track.get('user_id'),
                next_track,
                chat_id,
                next_track.get('user_name', 'Unknown'),
                chat_id,
                next_track.get('streamtype', 'audio'),
                next_track.get('quality', 'high')
            )
    except Exception as e:
        LOGGER(__name__).error(f"Error in stream end handler: {e}")

@tgcaller.on_closed_voice_chat()
async def on_voice_chat_closed_handler(client: TgCaller, update: Update):
    """Handle voice chat closed event"""
    chat_id = update.chat_id
    try:
        await remove_active_chat(chat_id)
        LOGGER(__name__).info(f"Voice chat closed in {chat_id}")
    except Exception as e:
        LOGGER(__name__).error(f"Error in voice chat closed handler: {e}")

@tgcaller.on_participant_change()
async def on_participant_change_handler(client: TgCaller, update: Update):
    """Handle participant change event"""
    chat_id = update.chat_id
    try:
        participants = await tgcaller.get_participants(chat_id)
        LOGGER(__name__).info(f"Participants changed in {chat_id}: {len(participants)} users")
        
        # Auto-leave if no participants
        if len(participants) <= 1:
            await Jhoom.stop_stream(chat_id)
            LOGGER(__name__).info(f"Auto-left {chat_id} due to no participants")
    except Exception as e:
        LOGGER(__name__).error(f"Error in participant change handler: {e}")

# Global plugin instance
jhoom_plugins = JhoomTgCallerPlugins()