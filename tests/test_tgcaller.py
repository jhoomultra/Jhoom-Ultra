"""
Pytest tests for TgCaller integration
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from JhoomMusic.core.call import JhoomCall
from JhoomMusic.plugins.tgcaller_handlers import JhoomTgCallerPlugins

@pytest.fixture
def jhoom_call():
    """Create JhoomCall instance for testing"""
    return JhoomCall()

@pytest.fixture
def jhoom_plugins():
    """Create JhoomTgCallerPlugins instance for testing"""
    return JhoomTgCallerPlugins()

class TestJhoomCall:
    """Test JhoomCall functionality"""
    
    @pytest.mark.asyncio
    async def test_start(self, jhoom_call):
        """Test TgCaller start"""
        with patch.object(jhoom_call.tgcaller, 'start', new_callable=AsyncMock) as mock_start:
            await jhoom_call.start()
            mock_start.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_pause_stream(self, jhoom_call):
        """Test pause stream functionality"""
        chat_id = 12345
        with patch.object(jhoom_call.tgcaller, 'pause_stream', new_callable=AsyncMock) as mock_pause:
            await jhoom_call.pause_stream(chat_id)
            mock_pause.assert_called_once_with(chat_id)
    
    @pytest.mark.asyncio
    async def test_resume_stream(self, jhoom_call):
        """Test resume stream functionality"""
        chat_id = 12345
        with patch.object(jhoom_call.tgcaller, 'resume_stream', new_callable=AsyncMock) as mock_resume:
            await jhoom_call.resume_stream(chat_id)
            mock_resume.assert_called_once_with(chat_id)
    
    @pytest.mark.asyncio
    async def test_join_call_audio(self, jhoom_call):
        """Test joining call with audio stream"""
        chat_id = 12345
        with patch.object(jhoom_call.tgcaller, 'join_group_call', new_callable=AsyncMock) as mock_join:
            with patch('JhoomMusic.utils.database.add_active_chat', new_callable=AsyncMock):
                await jhoom_call.join_call(
                    chat_id=chat_id,
                    original_chat_id=chat_id,
                    link="http://example.com/audio.mp3",
                    title="Test Song",
                    duration="3:30",
                    user_name="TestUser",
                    videoid="test123",
                    streamtype="audio",
                    quality="high"
                )
                mock_join.assert_called_once()
                assert chat_id in jhoom_call.active_calls
    
    @pytest.mark.asyncio
    async def test_join_call_video(self, jhoom_call):
        """Test joining call with video stream"""
        chat_id = 12345
        with patch.object(jhoom_call.tgcaller, 'join_group_call', new_callable=AsyncMock) as mock_join:
            with patch('JhoomMusic.utils.database.add_active_chat', new_callable=AsyncMock):
                await jhoom_call.join_call(
                    chat_id=chat_id,
                    original_chat_id=chat_id,
                    link="http://example.com/video.mp4",
                    title="Test Video",
                    duration="5:00",
                    user_name="TestUser",
                    videoid="test456",
                    streamtype="video",
                    quality="high"
                )
                mock_join.assert_called_once()
                assert chat_id in jhoom_call.active_calls
    
    @pytest.mark.asyncio
    async def test_stop_stream(self, jhoom_call):
        """Test stop stream functionality"""
        chat_id = 12345
        jhoom_call.active_calls[chat_id] = {"title": "Test"}
        
        with patch.object(jhoom_call.tgcaller, 'leave_group_call', new_callable=AsyncMock) as mock_leave:
            with patch('JhoomMusic.utils.database.remove_active_chat', new_callable=AsyncMock):
                await jhoom_call.stop_stream(chat_id)
                mock_leave.assert_called_once_with(chat_id)
                assert chat_id not in jhoom_call.active_calls
    
    @pytest.mark.asyncio
    async def test_skip_stream(self, jhoom_call):
        """Test skip stream functionality"""
        chat_id = 12345
        link = "http://example.com/next.mp3"
        
        with patch.object(jhoom_call.tgcaller, 'change_stream', new_callable=AsyncMock) as mock_change:
            await jhoom_call.skip_stream(chat_id, link, video=False)
            mock_change.assert_called_once()
    
    def test_is_connected(self, jhoom_call):
        """Test connection status check"""
        chat_id = 12345
        assert not jhoom_call.is_connected(chat_id)
        
        jhoom_call.active_calls[chat_id] = {"title": "Test"}
        assert jhoom_call.is_connected(chat_id)
    
    def test_get_call_info(self, jhoom_call):
        """Test getting call information"""
        chat_id = 12345
        call_info = {"title": "Test Song", "duration": "3:30"}
        
        assert jhoom_call.get_call_info(chat_id) is None
        
        jhoom_call.active_calls[chat_id] = call_info
        assert jhoom_call.get_call_info(chat_id) == call_info

class TestJhoomTgCallerPlugins:
    """Test TgCaller plugins functionality"""
    
    def test_plugin_initialization(self, jhoom_plugins):
        """Test plugin initialization"""
        assert jhoom_plugins.youtube_streamer is not None
        assert jhoom_plugins.bridge_manager is not None
    
    @pytest.mark.asyncio
    async def test_stream_youtube(self, jhoom_plugins):
        """Test YouTube streaming plugin"""
        chat_id = 12345
        url = "https://www.youtube.com/watch?v=test"
        
        with patch.object(jhoom_plugins.youtube_streamer, 'stream', new_callable=AsyncMock) as mock_stream:
            await jhoom_plugins.stream_youtube(chat_id, url, quality="high")
            mock_stream.assert_called_once_with(chat_id, url, "high")
    
    @pytest.mark.asyncio
    async def test_bridge_calls(self, jhoom_plugins):
        """Test call bridging plugin"""
        chat_id1 = 12345
        chat_id2 = 67890
        
        with patch.object(jhoom_plugins.bridge_manager, 'bridge', new_callable=AsyncMock) as mock_bridge:
            await jhoom_plugins.bridge_calls(chat_id1, chat_id2)
            mock_bridge.assert_called_once_with(chat_id1, chat_id2)

class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_playback_cycle(self, jhoom_call):
        """Test complete playback cycle"""
        chat_id = 12345
        
        # Mock all TgCaller methods
        with patch.object(jhoom_call.tgcaller, 'join_group_call', new_callable=AsyncMock):
            with patch.object(jhoom_call.tgcaller, 'pause_stream', new_callable=AsyncMock):
                with patch.object(jhoom_call.tgcaller, 'resume_stream', new_callable=AsyncMock):
                    with patch.object(jhoom_call.tgcaller, 'leave_group_call', new_callable=AsyncMock):
                        with patch('JhoomMusic.utils.database.add_active_chat', new_callable=AsyncMock):
                            with patch('JhoomMusic.utils.database.remove_active_chat', new_callable=AsyncMock):
                                
                                # Join call
                                await jhoom_call.join_call(
                                    chat_id=chat_id,
                                    original_chat_id=chat_id,
                                    link="http://example.com/test.mp3",
                                    title="Test Song",
                                    duration="3:30",
                                    user_name="TestUser",
                                    videoid="test123",
                                    streamtype="audio",
                                    quality="high"
                                )
                                
                                # Pause
                                await jhoom_call.pause_stream(chat_id)
                                
                                # Resume
                                await jhoom_call.resume_stream(chat_id)
                                
                                # Stop
                                await jhoom_call.stop_stream(chat_id)
                                
                                assert chat_id not in jhoom_call.active_calls

if __name__ == "__main__":
    pytest.main([__file__])