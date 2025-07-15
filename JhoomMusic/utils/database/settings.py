from JhoomMusic import db

settingsdb = db.settings

async def get_video_limit(chat_id: int) -> str:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "720"
    return mode["video_limit"]

async def get_playmode(chat_id: int) -> str:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "Direct"
    return mode["playmode"]

async def get_playtype(chat_id: int) -> str:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "Everyone"
    return mode["playtype"]

async def get_lang(chat_id: int) -> str:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "en"
    return mode["lang"]

async def save_lang(chat_id: int, lang: str):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"lang": lang}}, 
        upsert=True
    )

async def get_loop(chat_id: int) -> int:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return 0
    return mode["loop"]

async def set_loop(chat_id: int, mode: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"loop": mode}}, 
        upsert=True
    )

async def get_shuffle(chat_id: int) -> bool:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return False
    return mode["shuffle"]

async def set_shuffle(chat_id: int, mode: bool):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"shuffle": mode}}, 
        upsert=True
    )

async def is_music_playing(chat_id: int) -> bool:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return False
    return mode["playing"]

async def music_on(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"playing": True}}, 
        upsert=True
    )

async def music_off(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"playing": False}}, 
        upsert=True
    )

async def is_active_chat(chat_id: int) -> bool:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return False
    return mode["active"]

async def add_active_chat(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"active": True}}, 
        upsert=True
    )

async def remove_active_chat(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"active": False}}, 
        upsert=True
    )

async def is_video_allowed(chat_id: int) -> bool:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return True
    return mode["video_allowed"]

async def set_video_allowed(chat_id: int, mode: bool):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"video_allowed": mode}}, 
        upsert=True
    )

async def is_commanddelete_on(chat_id: int) -> bool:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return False
    return mode["command_delete"]

async def commanddelete_on(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"command_delete": True}}, 
        upsert=True
    )

async def commanddelete_off(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"command_delete": False}}, 
        upsert=True
    )

async def is_maintenance() -> bool:
    mode = await settingsdb.find_one({"chat_id": "maintenance"})
    if not mode:
        return False
    return mode["maintenance"]

async def maintenance_on():
    await settingsdb.update_one(
        {"chat_id": "maintenance"}, 
        {"$set": {"maintenance": True}}, 
        upsert=True
    )

async def maintenance_off():
    await settingsdb.update_one(
        {"chat_id": "maintenance"}, 
        {"$set": {"maintenance": False}}, 
        upsert=True
    )

async def get_assistant(chat_id: int) -> int:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return 1
    return mode["assistant"]

async def save_assistant(chat_id: int, assistant: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"assistant": assistant}}, 
        upsert=True
    )

async def get_audio_bitrate(chat_id: int) -> str:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "320"
    return mode["audio_bitrate"]

async def get_video_bitrate(chat_id: int) -> str:
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "720"
    return mode["video_bitrate"]

async def add_active_video_chat(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"video_active": True}}, 
        upsert=True
    )

async def remove_active_video_chat(chat_id: int):
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"video_active": False}}, 
        upsert=True
    )

async def get_active_chats():
    return settingsdb.find({"active": True})

async def get_active_video_chats():
    return settingsdb.find({"video_active": True})

# Group database for compatibility
group_db = {}

async def auto_clean(popped):
    """Clean up downloaded files"""
    try:
        if "file" in popped and os.path.exists(popped["file"]):
            os.remove(popped["file"])
    except:
        pass