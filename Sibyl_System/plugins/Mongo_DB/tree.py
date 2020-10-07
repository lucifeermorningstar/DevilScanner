from Sibyl_System import MONGO_CLIENT
from datetime import datetime

db = MONGO_CLIENT['Sibyl']['Main']

async def get_data() -> dict:
    data = await db.find_one({'_id': 4})
    return data

async def add_inspector(sibyl: int, inspector: int) -> True:
    data = await get_data()
    data[sibyl][inspector] = []
    data['standalone'][inspector] = {'addedby': sibyl, 'timestamp': datetime.timestamp(datetime.now())}
    await db.replace_one(await get_data(), data)

async def add_enforcers(inspector: int, enforcer: int) -> True:
    data = await get_data()
    sibyl = data['standalone'][inspector]['addedby']
    data[sibyl][inspector].append([enforcer])
    data['standalone'][enforcer] = {'addedby': inspector, 'timestamp': datetime.timestamp(datetime.now())}
    await db.replace_one(await get_data(), data)
    
