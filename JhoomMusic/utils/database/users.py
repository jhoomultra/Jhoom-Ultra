from typing import Dict, List, Union

from JhoomMusic import db

usersdb = db.users

async def get_served_users() -> list:
    users = []
    async for user in usersdb.find():
        users.append(user)
    return users

async def get_served_users_count() -> int:
    return await usersdb.count_documents({})

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})

async def remove_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if not is_served:
        return
    return await usersdb.delete_one({"user_id": user_id})