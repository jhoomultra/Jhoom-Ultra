import re
import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get it from my.telegram.org
API_ID = int(getenv("API_ID", "6701155507"))
API_HASH = getenv("API_HASH", "ee0b6a29d4918aa6dabeb181d2c15a36")

## Get it from @Botfather in Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "8000279573:AAGn2RZWvRzw5VKT2iska-_4kaWYVdfeJpI")

# Database to save your chats and stats... Get MongoDB:-  https://telegra.ph/How-To-get-Mongodb-URI-04-06
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://jhoommusic1:Ujala%404804@jhoommusic.mmccnwj.mongodb.net/?retryWrites=true&w=majority&appName=jhoommusic")

# Custom max audio(music) duration for voice chat. set DURATION_LIMIT in variables with your own time(mins), Default to 60 mins.
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "60"))

# Duration Limit for downloading Songs in MP3 or MP4 format from bot
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))

# You'll need a Private Group ID for this.
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002312345678"))

# Your User ID.
OWNER_ID = list(map(int, getenv("OWNER_ID", "5620922625").split()))

# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")

# You have to Enter the app name which you gave to identify your  Music Bot in Heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")

# For customized or modified Repository
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/TeamJhoom/JhoomMusicBot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

# GIT TOKEN ( if your edited repo is private)
GIT_TOKEN = getenv("GIT_TOKEN", "")

# Only  Links formats are  accepted for this Var value.
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/JhoomSupport")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/JhoomSupport")

# Set it in True if you want to leave your assistant after a certain amount of time. [Set time via AUTO_LEAVE_ASSISTANT_TIME]
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")

# Time after which you're assistant account will leave chats automatically.
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("AUTO_LEAVE_ASSISTANT_TIME", "5400"))

# Time after which bot will suggest random chats about bot commands.
AUTO_SUGGESTION_TIME = int(getenv("AUTO_SUGGESTION_TIME", "5400"))

# Set it True if you want to delete downloads after the music playout ends from your downloads folder
AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", "True")

# Set it True if you want to bot to suggest about bot commands to random chats of your bots.
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "True")

# You'll need a Pyrogram String Session for these vars. Generate String from our session generator bot @JhoomStringBot
STRING1 = getenv("STRING_SESSION", "BQF_OdsAJJCB9ILaOmRp7lERmO95xwM-drzLUFFvjsS9dnK4lqpH1f45yv7ulo53LspWP0Yx5Z5hdS31X77kgA2fxVs6ZqiARG4KYjwN8n8Czr0qSwdQfc-8O85V183sQpJRa6QRjrZG6vqU-NvJID2kjp6tz39WHv8MK7weIF5HmCEaTKblSvNIzC82vwR5mI1ygvinzRlA5QL4e7O4j35cNELs1RiwSRkwWRbyTzQSX0MY-krYi3L6QKYLZA2qfEzTtAyqQQtoMpVvzqwCHbIMw27li0EuacsLiqSYfnIbOuCiK8Rilk7XVtXZ7JVUg779v-MkERi94oqQXzPJH6Co6b_TQgAAAAGPa4SzAA")
STRING2 = getenv("STRING_SESSION2", "")
STRING3 = getenv("STRING_SESSION3", "")
STRING4 = getenv("STRING_SESSION4", "")
STRING5 = getenv("STRING_SESSION5", "")

# Only Alpha-Numeric characters are allowed. If you don't know about it, then leave it as it is.
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "5"))

# Telegram audio  and video file size limit
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824"))

# If you want your bot to setup the commands automatically in the bot's menu set it to true.
# Refer to https://i.postimg.cc/Fzg9vcs2/image.png
SET_CMDS = getenv("SET_CMDS", "False")

# You'll need a Spotify Client.. checkout https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "07e0249e87044dd69b20bfa841ff2d24")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "d38e214ff06e43a386fc20d4fa02ab88")

# Maximum number of video calls allowed on bot. You can later set it via /set_video_limit on telegram
VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "3"))

# Maximum Limit Allowed for users to save playlists on bot's server
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "30"))

# MaximuM limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Bot name
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "Jhoom Music")

BANNED_USERS = filters.user()
YTDOWNLOADER = 1
LOG = 2
LOG_FILE_NAME = "JhoomLogs.txt"
adminlist = {}
lyrical = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

# Images
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
GLOBAL_IMG_URL = getenv("GLOBAL_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://telegra.ph/file/c0e014ff34f34d1056627.png")

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        print("[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://")
        sys.exit()

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        print("[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://")
        sys.exit()

if UPSTREAM_REPO:
    if not re.match("(?:http|https)://", UPSTREAM_REPO):
        print("[ERROR] - Your UPSTREAM_REPO url is wrong. Please ensure that it starts with https://")
        sys.exit()