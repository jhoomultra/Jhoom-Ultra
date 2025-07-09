from typing import Dict, List, Union

from YukkiMusic import db

usersdb = db.users


async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)


async def get_served_users() -> list:
    users = usersdb.find({"user_id": {"$gt": 0}})
    return [user["user_id"] async for user in users]


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


async def get_banned_users() -> list:
    users = usersdb.find({"banned": True})
    return [user["user_id"] async for user in users]


async def add_banned_user(user_id: int):
    is_served = await is_served_user(user_id)
    if not is_served:
        await add_served_user(user_id)
    return await usersdb.update_one(
        {"user_id": user_id}, {"$set": {"banned": True}}
    )


async def remove_banned_user(user_id: int):
    is_served = await is_served_user(user_id)
    if not is_served:
        await add_served_user(user_id)
    return await usersdb.update_one(
        {"user_id": user_id}, {"$set": {"banned": False}}
    )