from typing import Dict, List, Union

from YukkiMusic import db

sudodb = db.sudo


async def get_sudoers() -> list:
    sudoers = sudodb.find({"sudo": True})
    return [sudoer["user_id"] async for sudoer in sudoers]


async def get_gbanned() -> list:
    results = []
    async for user in sudodb.find({"gbanned": True}):
        results.append(user["user_id"])
    return results


async def is_gbanned_user(user_id: int) -> bool:
    user = await sudodb.find_one({"user_id": user_id})
    return user.get("gbanned", False) if user else False


async def add_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return
    return await sudodb.update_one(
        {"user_id": user_id}, {"$set": {"gbanned": True}}, upsert=True
    )


async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return
    return await sudodb.update_one(
        {"user_id": user_id}, {"$set": {"gbanned": False}}, upsert=True
    )


async def is_sudo(user_id: int) -> bool:
    user = await sudodb.find_one({"user_id": user_id})
    return user.get("sudo", False) if user else False


async def add_sudo(user_id: int):
    is_sudo_user = await is_sudo(user_id)
    if is_sudo_user:
        return
    return await sudodb.update_one(
        {"user_id": user_id}, {"$set": {"sudo": True}}, upsert=True
    )


async def remove_sudo(user_id: int):
    is_sudo_user = await is_sudo(user_id)
    if not is_sudo_user:
        return
    return await sudodb.update_one(
        {"user_id": user_id}, {"$set": {"sudo": False}}, upsert=True
    )