from typing import Dict, List, Union

from YukkiMusic import db

playlistdb = db.playlist


async def get_playlist_names(user_id: int) -> List[str]:
    results = []
    async for playlist in playlistdb.find({"user_id": user_id}):
        results.append(playlist["playlist_name"])
    return results


async def get_playlist(user_id: int, name: str) -> Dict:
    playlist = await playlistdb.find_one(
        {"user_id": user_id, "playlist_name": name}
    )
    return playlist if playlist else {}


async def save_playlist(
    user_id: int, name: str, title: str, duration: str, videoid: str, username: str
):
    playlist = await playlistdb.find_one(
        {"user_id": user_id, "playlist_name": name}
    )
    if playlist:
        await playlistdb.update_one(
            {"user_id": user_id, "playlist_name": name},
            {
                "$push": {
                    "tracks": {
                        "title": title,
                        "duration": duration,
                        "videoid": videoid,
                        "by": username,
                    }
                }
            },
        )
    else:
        await playlistdb.insert_one(
            {
                "user_id": user_id,
                "playlist_name": name,
                "tracks": [
                    {
                        "title": title,
                        "duration": duration,
                        "videoid": videoid,
                        "by": username,
                    }
                ],
            }
        )


async def delete_playlist(user_id: int, name: str):
    await playlistdb.delete_one({"user_id": user_id, "playlist_name": name})


async def delete_playlist_track(user_id: int, name: str, title: str):
    await playlistdb.update_one(
        {"user_id": user_id, "playlist_name": name},
        {"$pull": {"tracks": {"title": title}}},
    )