from Sibyl_System import System, session, INSPECTORS, Sibyl_logs
from Sibyl_System.strings import proof_string, scan_request_string
from Sibyl_System.plugins.Mongo_DB.gbans import get_gban

from telethon import custom
from telethon import events

import re
import asyncio

data = []
DATA_LOCK = asyncio.Lock()


async def make_proof(user):
    data = await get_gban(user)
    if not data:
        return False
    message = data.get('message') or ''
    async with session.post('https://nekobin.com/api/documents', json={'content': message}) as r:
        paste = f"https://nekobin.com/{(await r.json())['result']['key']}"
    url = "https://del.dog/documents"
    async with session.post(url, data=message.encode("UTF-8")) as f:
         r = await f.json()
         url = f"https://del.dog/{r['key']}"
    return proof_string.format(proof_id = data['proof_id'], reason=data['reason'], paste=paste, url=url)

@System.bot.on(events.NewMessage(pattern = "[/?]start"))
async def sup(event):
    await event.reply('sup?')

@System.bot.on(events.NewMessage(pattern = "[/?]help"))
async def help(event):
    await event.reply("""
This bot is a inline bot, You can use it by typing `@SibylSystemRobot`
If a user is gbanned -
    Getting reason for gban, message the user was gbanned for - `@SibylSystemRobot proof <user_id>`
    """)


@System.bot.on(events.InlineQuery)  # pylint:disable=E0602
async def inline_handler(event):
    builder = event.builder
    query = event.text
    split = query.split(' ', 1)
    if event.query.user_id not in INSPECTORS:
        result = builder.article("Sibyl System", text = "You don't have access to this cmd.")
        await event.answer([result])
        return
    if query.startswith("proof"):
      if len(split) == 1:
         result = builder.article("Type Case-ID", text="No Case-ID was provided")
      else:
         proof = await make_proof(int(split[1]))
         if proof is False:
            result = builder.article("Unknown error occured while getting proof from Case-ID",
                                     text="Unknown error occured while getting proof from Case-ID")
         else:
            result = builder.article("Proof", text = proof, link_preview=False)
    elif query.startswith("builder"):
      split = query.replace('builder', '').split(':::', 4)
      print(split)
      if len(split) != 5:
          result = builder.article('Not enough info provided...')
      else:
          u_id, enforcer, source, reason, message = split
          dict_ = {'u_id': u_id, "enforcer": enforcer, "source": source, "reason": reason, "message": message}
          print(dict_)
          async with DATA_LOCK:
              data.append(dict_)
              index = data.index(dict_)
          buttons = [custom.Button.inline("Approve", data = f"approve_{index}"), custom.Button.inline("Reject", data = f"reject_{index}")]
          result = builder.article(
                "Output",
                text = scan_request_string.format(enforcer = enforcer, spammer = u_id, reason = reason, chat = source, message = message),
                buttons = buttons
          )

    else:
        result = builder.article("No type provided", text="Use\nproof <user_id> to get proof\nbuilder id:::enforcer:::source:::reason:::message")
    await event.answer([result])
