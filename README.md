# 🎵 Jhoom Music Bot

A powerful Telegram music bot with advanced features for playing music in voice chats.

## ✨ Features

- 🎵 High-quality music streaming
- 🎬 Video playback support
- 📱 Multiple platform support (YouTube, Spotify, SoundCloud)
- 🎛️ Interactive player controls
- 📋 Queue management
- 🔄 Loop and shuffle functionality
- 👥 Admin controls
- 🎨 Beautiful thumbnails
- 🔧 Self-repair system
- 📊 Statistics and monitoring

## 🚀 Deployment

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TeamJhoom/JhoomMusicBot)

### Local Deployment

1. Clone the repository:
```bash
git clone https://github.com/TeamJhoom/JhoomMusicBot
cd JhoomMusicBot
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

4. Run the bot:
```bash
python3 main.py
```

## 📋 Commands

### Basic Commands
- `/play` - Play music from YouTube/Spotify
- `/vplay` - Play video in voice chat
- `/pause` - Pause current playback
- `/resume` - Resume paused playback
- `/skip` - Skip to next track
- `/stop` - Stop playback and clear queue

### Admin Commands
- `/auth` - Authorize users
- `/broadcast` - Broadcast messages
- `/gban` - Global ban users
- `/maintenance` - Toggle maintenance mode

### Settings
- `/settings` - Open settings panel
- `/loop` - Toggle loop mode
- `/shuffle` - Shuffle queue

## 🔧 Configuration

Required environment variables:
- `API_ID` - Get from my.telegram.org
- `API_HASH` - Get from my.telegram.org
- `BOT_TOKEN` - Get from @BotFather
- `MONGO_DB_URI` - MongoDB connection string
- `STRING_SESSION` - Pyrogram session string
- `OWNER_ID` - Your user ID
- `LOG_GROUP_ID` - Log group ID

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

- Support Group: [@JhoomSupport](https://t.me/JhoomSupport)
- Updates Channel: [@JhoomMusicUpdates](https://t.me/JhoomMusicUpdates)

## ⭐ Credits

- [Pyrogram](https://github.com/pyrogram/pyrogram)
- [Py-TgCalls](https://github.com/pytgcalls/pytgcalls)
- [YT-DLP](https://github.com/yt-dlp/yt-dlp)