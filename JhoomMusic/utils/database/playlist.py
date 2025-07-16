from typing import Dict, List, Union

from JhoomMusic import db

playlistdb = db.playlist

async def get_playlist_count() -> int:
    return await playlistdb.count_documents({})

async def get_playlist(user_id: int):
    return await playlistdb.find_one({"user_id": user_id})

async def save_playlist(user_id: int, playlist_name: str, playlist: list):
    await playlistdb.update_one(
        {"user_id": user_id, "playlist_name": playlist_name},
        {"$set": {"playlist": playlist}},
        upsert=True
    )

async def delete_playlist(user_id: int, playlist_name: str):
    await playlistdb.delete_one({"user_id": user_id, "playlist_name": playlist_name})