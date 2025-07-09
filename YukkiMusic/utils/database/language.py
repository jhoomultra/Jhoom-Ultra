from YukkiMusic import db

langdb = db.language


async def get_lang(chat_id: int) -> str:
    mode = await langdb.find_one({"chat_id": chat_id})
    if not mode:
        return "en"
    return mode["lang"]


async def set_lang(chat_id: int, lang: str):
    mode = await langdb.find_one({"chat_id": chat_id})
    if not mode:
        await langdb.insert_one({"chat_id": chat_id, "lang": lang})
    else:
        await langdb.update_one(
            {"chat_id": chat_id}, {"$set": {"lang": lang}}
        )