from JhoomMusic import db

langdb = db.language

async def get_lang(chat_id: int) -> str:
    mode = await langdb.find_one({"chat_id": chat_id})
    if not mode:
        return {"language": "en"}
    return mode

async def set_lang(chat_id: int, language: str):
    await langdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"language": language}}, 
        upsert=True
    )