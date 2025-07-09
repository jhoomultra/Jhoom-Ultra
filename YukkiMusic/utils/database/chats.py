from typing import Dict, List, Union

from YukkiMusic import db

chatsdb = db.chats


async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    return [chat["chat_id"] async for chat in chats]


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return bool(chat)


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"chat_id": chat_id})


async def blacklisted_chats() -> list:
    chats = chatsdb.find({"blacklisted": True})
    return [chat["chat_id"] async for chat in chats]


async def blacklist_chat(chat_id: int):
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
    return await chatsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"blacklisted": True}}
    )


async def whitelist_chat(chat_id: int):
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
    return await chatsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"blacklisted": False}}
    )


async def get_active_chats() -> list:
    return []


async def add_active_chat(chat_id: int):
    pass


async def remove_active_chat(chat_id: int):
    pass