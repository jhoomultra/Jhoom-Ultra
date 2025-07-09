from typing import Dict, List, Union

queues: Dict[int, List[Dict]] = {}


async def put_queue(
    chat_id: int,
    original_chat_id: int,
    file: str,
    title: str,
    duration: str,
    user: str,
    videoid: str,
    user_id: int,
    stream: str,
):
    put = {
        "title": title,
        "dur": duration,
        "by": user,
        "user_id": user_id,
        "videoid": videoid,
        "file": file,
        "stream": stream,
        "original_chat_id": original_chat_id,
    }
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append(put)


async def get_queue(chat_id: int) -> Union[Dict, bool]:
    if chat_id in queues:
        if len(queues[chat_id]) >= 1:
            return queues[chat_id][0]
    return False


async def pop_an_item(chat_id: int) -> Union[Dict, bool]:
    if chat_id in queues:
        if len(queues[chat_id]) >= 1:
            return queues[chat_id].pop(0)
    return False


async def is_empty_queue(chat_id: int) -> bool:
    if chat_id in queues:
        if len(queues[chat_id]) >= 1:
            return False
    return True


async def task_queue(chat_id: int) -> int:
    if chat_id in queues:
        return len(queues[chat_id])
    return 0


async def clear_queue(chat_id: int):
    if chat_id in queues:
        queues[chat_id].clear()
    return True


async def shuffle_queue(chat_id: int):
    if chat_id in queues:
        import random
        random.shuffle(queues[chat_id])
    return True


async def put_queue_index(
    chat_id: int,
    original_chat_id: int,
    file: str,
    title: str,
    duration: str,
    user: str,
    videoid: str,
    user_id: int,
    stream: str,
    index: int,
):
    put = {
        "title": title,
        "dur": duration,
        "by": user,
        "user_id": user_id,
        "videoid": videoid,
        "file": file,
        "stream": stream,
        "original_chat_id": original_chat_id,
    }
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].insert(index, put)