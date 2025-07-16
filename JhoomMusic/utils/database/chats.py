from typing import Dict, List, Union

from JhoomMusic import db

chatsdb = db.chats

async def get_served_chats() -> list:
    chats = []
    async for chat in chatsdb.find():
        chats.append(chat)
    return chats

async def get_served_chats_count() -> int:
    return await chatsdb.count_documents({})

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