from Sibyl_System import System, system_cmd
from telethon import events
from Sibyl_System import INSPECTORS
import Sibyl_System.plugins.Mongo_DB.gbans as db

@System.on(system_cmd(pattern=r'proof ', allow_inspectors=True))
async def proof(event):
        msg = await System.send_message(event.chat_id, 'Connecting to archive for case file >>>>>')
        try:
            proof_id = int(event.text.split(' ', 1)[1])
        except BaseException:
            await msg.edit('>>>>>The case file ID is invalid')
            return
        await msg.edit('Fetching msg details from case file ID <<<<<<<')
        proof = await System.get_messages(Sibyl_logs, ids=proof_id)
        try:
            reason = re.search(r"(\*\*)?Scan Reason:(\*\*)? (`([^`]*)`|.*)", proof.message)
            reason = reason.group(4) if reason.group(4) else reason.group(3)
        except BaseException:
            await msg.edit('>>>>Unable to see the msg or the case file ID is not valid')
            return
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
                        await msg.edit('Case file includes media -> Forwarding message') 
                        await proof.forward_to(event.chat_id)
                        return
                    else:
                        await msg.edit(f"Error getting case file from ID {proof_id}")
                        return
                else:
                    await msg.edit(f" Failed to pull case file, Is the ID valid?")
                    return
        async with session.post('https://nekobin.com/api/documents', json={'content': message}) as r:
            paste = f"https://nekobin.com/{(await r.json())['result']['key']}"
        url = "https://del.dog/documents"
        async with session.post(url, data=message.encode("UTF-8")) as f:
             r = await f.json()
             url = f"https://del.dog/{r['key']}"
        await msg.edit(proof_string.format(proof_id = proof_id, reason=reason, paste=paste, url=url))

@System.bot.on(events.InlineQuery)  # pylint:disable=E0602
async def inline_handler(event):
  builder = event.builder
  query = event.text
  split = query.split(' ', 1)
  if event.query.user_id not in INSPECTORS:
    result = builder.article("You don't have access to this cmd.")
    await event.answer(result)
    return
  if query.startswith("qproof"):
    if len(split) == 1:
      result = builder.article("Type User id")
    else:
      user_data = await db.get_gban(int(split[1]))
      if not user_data:
         result = builder.article('User is not gbanned')
      else:
         result =  f"User: {user_data['user']}\n"\
                   f"Enforcer: {user_data['enforcer']}\n"\
                   f"Reason: {user_data['reason']}\n"\
                   f"Extended Proof: {user_data['proof_id']}"
         result = builder.article(result)
    await event.answer('Sibyl System DB', text = result)
