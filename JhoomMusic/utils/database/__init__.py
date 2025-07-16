from .chats import *
from .language import *
from .playlist import *
from .queue import *
from .sudo import *
from .users import *
from .settings import *

# Additional database functions
async def add_sudo(user_id: int):
    from JhoomMusic import db
    sudodb = db.sudo
    await sudodb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_banned_users():
    from JhoomMusic import db
    banned = db.banned_users
    users = []
    async for user in banned.find():
        users.append(user["user_id"])
    return users

async def get_gbanned():
    from JhoomMusic import db
    gbanned = db.gbanned_users
    users = []
    async for user in gbanned.find():
        users.append(user["user_id"])
    return users

async def add_served_chat(chat_id: int):
    from JhoomMusic import db
    chatsdb = db.chats
    await chatsdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True
    )

async def add_served_user(user_id: int):
    from JhoomMusic import db
    usersdb = db.users
    await usersdb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )