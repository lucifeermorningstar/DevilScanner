from Sibyl_System import System, system_cmd
from telethon import events
from Sibyl_System import INSPECTORS, Sibyl_logs
import Sibyl_System.plugins.Mongo_DB.gbans as db
import asyncio

async def make_proof(event, proof_id):
        proof = await System.get_messages(Sibyl_logs, ids=proof_id)
        try:
            reason = re.search(r"(\*\*)?Scan Reason:(\*\*)? (`([^`]*)`|.*)", proof.message)
            reason = reason.group(4) if reason.group(4) else reason.group(3)
        except BaseException:
            return "Invalid"
        try:
            message = re.search(
                '(\*\*)?Target Message:(\*\*)? (.*)',
                proof.message,
                re.DOTALL).group(3)
        except BaseException:
                proof_id -= 1
                proof = await System.get_messages(Sibyl_logs, ids=proof_id)
                if proof:
                    if proof.media:
                        return "Media"
                    else:
                        return False
                else:
                    return False
        async with session.post('https://nekobin.com/api/documents', json={'content': message}) as r:
            paste = f"https://nekobin.com/{(await r.json())['result']['key']}"
        url = "https://del.dog/documents"
        async with session.post(url, data=message.encode("UTF-8")) as f:
             r = await f.json()
             url = f"https://del.dog/{r['key']}"
        return proof_string.format(proof_id = proof_id, reason=reason, paste=paste, url=url)

@System.bot.on(events.InlineQuery)  # pylint:disable=E0602
async def inline_handler(event):
  builder = event.builder
  query = event.text
  split = query.split(' ', 1)
  if event.query.user_id not in INSPECTORS:
    result = builder.article("Sibyl System", text = "You don't have access to this cmd.")
    await event.answer([result])
    return
  await asyncio.sleep(2)
  if query.startswith("qproof"):
    if len(split) == 1:
      result = builder.article("Type User id", text="No Id was proved")
    else:
      user_data = await db.get_gban(int(split[1]))
      if not user_data:
         result = builder.article('User is not gbanned', text = f'User[{split[1]}] is not gbanned')
      else:
         result =  f"User: {user_data['user']}\n"\
                   f"Enforcer: {user_data['enforcer']}\n"\
                   f"Reason: {user_data['reason']}\n"\
                   f"Extended Proof: {user_data['proof_id']}"
         result = builder.article('Quick-Proof', text = result)
  elif query.startswith("proof"):
      if len(split) == 1:
         result = builder.article("Type Case-ID", text="No Case-ID was provided")
      else:
         proof = await make_proof(event, int(split[1]))
         if proof == "Invalid":
            result = builder.article("Invalid  Case-ID", text="Case-ID is Invalid")
         elif proof == "Media":
            result = builder.article("The provided message was media",
                                     text="The provided proof was Media, You will have to manually get proof")
         elif proof is False:
            result = builder.article("Unknown error occured while getting proof from Case-ID",
                                     text="Unknown error occured while getting proof from Case-ID")
         else:
            result = builder.article("Proof", text = proof, link_preview=False)                              
  await event.answer([result])
