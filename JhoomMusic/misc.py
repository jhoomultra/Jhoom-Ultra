import config
from JhoomMusic.utils.database import add_sudo

from .logging import LOGGER

SUDOERS = []

async def sudo():
    global SUDOERS
    SUDOERS.clear()
    
    # Add owner IDs to sudo list
    for user_id in config.OWNER_ID:
        SUDOERS.append(user_id)
        await add_sudo(user_id)
    
    LOGGER(__name__).info(f"Loaded {len(SUDOERS)} sudo users")