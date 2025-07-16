from typing import Dict, List, Union

from JhoomMusic import db

sudodb = db.sudo

async def get_sudoers() -> list:
    sudoers = []
    async for user in sudodb.find():
        sudoers.append(user["user_id"])
    return sudoers

async def add_sudo(user_id: int) -> bool:
    sudoer = await sudodb.find_one({"user_id": user_id})
    if sudoer:
        return False
    return bool(await sudodb.insert_one({"user_id": user_id}))

async def remove_sudo(user_id: int) -> bool:
    sudoer = await sudodb.find_one({"user_id": user_id})
    if not sudoer:
        return False
    return bool(await sudodb.delete_one({"user_id": user_id}))