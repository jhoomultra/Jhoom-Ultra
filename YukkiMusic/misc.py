import config
from YukkiMusic.utils.database import add_sudo

from .logging import LOGGER


async def sudo():
    if config.OWNER_ID:
        for user_id in config.OWNER_ID:
            await add_sudo(user_id)
    LOGGER(__name__).info(f"Sudo Users Loaded.")