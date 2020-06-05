from Sibyl_System import MONGO_CLIENT

db = MONGO_CLIENT['Sibyl']['Main']

async def get_gbans() -> dict:
    json = await db.find_one({'_id': 3})
    return json

async def get_gban(user:int) :
    gbans = await get_gbans()
    if user not in gbans['victim']:
        return False
    else:
        place = user.index(gbans['victim'])
        user_data = {}
        user_data['user'] = gbans['victim'][place]
        user_data['reason'] = gbans['reason'][place]
        user_data['enforcer'] = gbans['gbanners'][place]
        user_data['proof_id'] = gbans['proof_id'][place]
        return user_data
        

async def update_gban(victim:int, reason:str=None, proof_id:int=None, enforcer:int=None, add:bool=True) -> bool:
    gbans_dict = await get_gbans()
    if victim not in gbans_dict['victim'] and not add:
        return False
    if victim in gbans_dict['victim'] and add:
        return False
    if add:
        gbans_dict['victim'].append(victim)
        gbans_dict['reason'].append(reason)
        gbans_dict['proof_id'].append(proof_id)
        gbans_dict['gbanners'].append(enforcer)
    else:
        gbans_dict['victim'].remove(victim)
        gbans_dict['reason'].remove(reason)
        gbans_dict['proof_id'].remove(proof_id)
        gbans_dict['gbanners'].remove(enforcer)
    await db.replace_one(await get_gbans(), gbans_dict)
    return True
