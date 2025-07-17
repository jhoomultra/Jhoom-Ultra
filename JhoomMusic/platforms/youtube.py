import asyncio
import os
import re
import yt_dlp
from typing import Union, List, Dict, Optional
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        """Check if YouTube URL exists"""
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1) -> Union[str, None]:
        """Extract URL from message"""
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == "url":
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == "url":
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
        if offset in (None,):
            return None
        url = text[offset : offset + length]
        if await self.exists(url):
            return url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None) -> tuple:
        """Get video details"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                duration_min = f"{duration//60}:{duration%60:02d}" if duration else "Live"
                thumbnail = info.get('thumbnail', '')
                vidid = info.get('id', 'unknown')
                
                return title, duration_min, duration, thumbnail, vidid
        except Exception as e:
            print(f"Error getting details: {e}")
            return "Unknown", "00:00", 0, "", "unknown"

    async def title(self, link: str, videoid: Union[bool, str] = None) -> str:
        """Get video title"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get('title', 'Unknown')
        except:
            return "Unknown"

    async def duration(self, link: str, videoid: Union[bool, str] = None) -> str:
        """Get video duration"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                duration = info.get('duration', 0)
                return f"{duration//60}:{duration%60:02d}" if duration else "Live"
        except:
            return "Unknown"

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None) -> str:
        """Get video thumbnail"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get('thumbnail', '')
        except:
            return ""

    async def video(self, link: str, videoid: Union[bool, str] = None) -> tuple:
        """Get video stream URL"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            ydl_opts = {
                'format': 'best[height<=?720][width<=?1280]',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                url = info.get('url', '')
                return 1, url
        except Exception as e:
            return 0, str(e)

    async def track(self, link: str, videoid: Union[bool, str] = None) -> tuple:
        """Get audio track info and URL"""
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                duration_min = f"{duration//60}:{duration%60:02d}" if duration else "Live"
                vidid = info.get('id', 'unknown')
                yturl = info.get('webpage_url', link)
                thumbnail = info.get('thumbnail', '')
                url = info.get('url', '')
                
                track_details = {
                    "title": title,
                    "link": url,
                    "vidid": vidid,
                    "duration_min": duration_min,
                    "duration_sec": duration,
                    "thumb": thumbnail,
                    "url": url
                }
                return track_details, vidid
        except Exception as e:
            print(f"Error getting track: {e}")
            return None, None

    async def search(self, query: str, filter: bool = False, videoid: Union[bool, str] = None) -> List[Dict]:
        """Search YouTube videos"""
        if videoid:
            query = self.base + query
        
        try:
            results = YoutubeSearch(query, max_results=10).to_dict()
            formatted_results = []
            
            for result in results:
                formatted_result = {
                    'title': result.get('title', 'Unknown'),
                    'id': result.get('id', 'unknown'),
                    'url': f"https://youtube.com{result.get('url_suffix', '')}",
                    'duration': result.get('duration', '00:00'),
                    'duration_seconds': self._duration_to_seconds(result.get('duration', '00:00')),
                    'thumbnail': result.get('thumbnails', [{}])[0].get('url', '') if result.get('thumbnails') else '',
                    'channel': result.get('channel', 'Unknown'),
                    'views': result.get('views', '0')
                }
                formatted_results.append(formatted_result)
            
            return formatted_results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def _duration_to_seconds(self, duration_str: str) -> int:
        """Convert duration string to seconds"""
        try:
            if ':' in duration_str:
                parts = duration_str.split(':')
                if len(parts) == 2:
                    return int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return 0
        except:
            return 0

    async def download(
        self,
        link: str,
        mystic,
        videoid: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ) -> str:
        """Download audio/video"""
        if videoid:
            link = self.base + link
        
        loop = asyncio.get_running_loop()
        
        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio[ext=m4a]",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        if video:
            downloaded_file = await loop.run_in_executor(None, video_dl)
        else:
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file

# Global instance
YouTube = YouTubeAPI()