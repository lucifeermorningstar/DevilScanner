from Sibyl_System import MONGO_CLIENT
from typing import Optional, Dict, Union

db = MONGO_CLIENT["SibylSystemRobot"]["Main"]

async def get_chat(chat: int) -> Optional[Dict[str, Union[str, int]]]:
    settings = await db.find_one({'chat_id': chat})
    return settings

async def add_chat(chat: int) -> bool:
    exists = await db.find_one({'chat_id': chat})
    if exists:
        return False
    await db.insert_one({'chat_id': chat, 'alert': True, 'alertmode': 'warn'})
    return True
