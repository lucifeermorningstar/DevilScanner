from Sibyl_System import Sibyl_logs, ENFORCERS, SIBYL, INSPECTORS, GBAN_MSG_LOGS
from Sibyl_System.strings import scan_request_string, scan_approved_string, bot_gban_string, reject_string, proof_string, forced_scan_string
from Sibyl_System import System, system_cmd
from Sibyl_System import session
from Sibyl_System.utils import seprate_flags
import Sibyl_System.plugins.Mongo_DB.gbans as db

import re
import logging


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)

url_regex = re.compile('(http(s)?://)?t.me/(c/)?(\w+)/(\d+)')

def get_data_from_url(url: str) -> tuple:
      """
      >>> get_data_from_url("https://t.me/c/1476401326/36963")
      (1476401326, 36963)
      """
      match = url_regex.match(url)
      if not match:
        return False
      return (match.group(4), match.group(5))
      


@System.on(system_cmd(pattern=r'scan ', allow_enforcer = True))
async def scan(event):
        trim = None
        replied = await event.get_reply_message()
        flags, reason = seprate_flags(event.text)
        if len(reason.split(" ", 1)) == 1:
          return
        split = reason.strip().split(" ", 1)
        reason = reason.strip().split(" ", 1)[1]
        if 'u' in flags.keys():
           url = reason
           data = get_data_from_url(url.strip())
           if not data:
              await event.reply('Invalid url')
              return
           try:
              message = await System.get_messages(int(data[0]) if data[0].isnumeric() else data[0], ids = int(data[1]))
           except:
              await event.reply('Failed to get data from url')
              return
           executor = await event.get_sender()
           executor = f'[{executor.first_name}](tg://user?id={executor.id})'
           if not message:
              await event.reply('Failed to get data from url')
              return
           if message.from_id in ENFORCERS:
              return
           msg = await System.send_message(Sibyl_logs, scan_request_string.format(enforcer=executor, spammer=message.from_id, chat=url.split(" ", 1)[0] , message=message.text, reason=split[1].strip().split(' ')[1]))
           return
        if not event.is_reply:
          return
        if 'o' in flags.keys():
            if replied.fwd_from:
                reply = replied.fwd_from
                target = reply.from_id
                if reply.from_id in ENFORCERS or reply.from_id in SIBYL:
                    return
                if not reply.from_id:
                    await event.reply("Cannot get user ID.")
                    return
                if reply.from_name:
                    sender = f"[{reply.from_name}](tg://user?id={reply.from_id})"
                else:
                    sender = f"[{reply.from_id}](tg://user?id={reply.from_id})"
        else:
            if replied.sender.id in ENFORCERS:
                return
            sender = f"[{replied.sender.first_name}](tg://user?id={replied.sender.id})"
            target = replied.sender.id
        executer = await event.get_sender()
        req_proof = req_user = False
        if 'f' in flags.keys() and executer.id in INSPECTORS:
             approve = True
        else:
             approve = False
        match = re.match('.scan -f -p (\d+) .*', event.text)
        if replied.video or replied.document or replied.contact or replied.gif or replied.sticker:
            await replied.forward_to(Sibyl_logs)
        executor = f'[{executer.first_name}](tg://user?id={executer.id})'
        chat = f"t.me/{event.chat.username}/{event.message.id}" if event.chat.username else f"t.me/c/{event.chat.id}/{event.message.id}"
        await event.reply("Connecting to Sibyl for a cymatic scan.")
        if req_proof and req_user:
           await replied.forward_to(Sibyl_logs)
           await System.gban(executer.id, req_user, reason, msg.id, executer)
        if not approve:
           msg = await System.send_message(Sibyl_logs, scan_request_string.format(enforcer=executor, spammer=sender, chat=chat , message=replied.text, reason=reason))
           return
        msg = await System.send_message(Sibyl_logs, forced_scan_string.format(ins = executor, spammer=sender, chat=chat,message=replied.text, reason=reason))
        await System.gban(executer.id, target, reason, msg.id, executer)

@System.on(system_cmd(pattern=r're(vive|vert|store) '))
async def revive(event):
   try:
     user_id = event.text.split(" ", 1)[1]
   except IndexError: return
   a = await event.reply("Reverting bans..")
   await System.ungban(user_id, f" By //{(await event.get_sender()).id}")
   await a.edit("Revert request sent to sibyl. This might take 10minutes or so.")


@System.on(system_cmd(pattern=r'approve', allow_inspectors=True, force_reply = True))
async def approve(event):
        replied = await event.get_reply_message()
        match = re.match(r'\$SCAN', replied.text)
        auto_match = re.search(r'\$AUTO(SCAN)?', replied.text)
        me = await System.get_me()
        if auto_match:
            if replied.sender.id == me.id:
                id = re.search(
                    r"\*\*Scanned user\*\*: (\[\w+\]\(tg://user\?id=(\d+)\)|(\d+))",
                    replied.text).group(2)
                try:
                     bot = (await System.get_entity(id)).bot
                except:
                     bot = False
                reason = re.search('\*\*Reason:\*\* (.*)', replied.text).group(1)
                await System.gban(enforcer=me.id, target=id, reason = reason, msg_id=replied.id, auto=True, bot=bot)
                return "OwO"
        if match:
            reply = replied.sender.id
            sender = await event.get_sender()
            # checks to not gban the Gbanner and find who is who
            if reply == me.id:
                list = re.findall(r'tg://user\?id=(\d+)', replied.text)
                reason = re.search(r"(\*\*)?Scan Reason:(\*\*)? (`([^`]*)`|.*)", replied.text)
                reason = reason.group(4) if reason.group(4) else reason.group(3)
                if len(list) > 1:
                    id1 = list[0]
                    id2 = list[1]
                else:
                    id1 = list[0]
                    id2 = re.findall(r'(\d+)', replied.text)[1]
                if id1 in ENFORCERS or SIBYL:
                    enforcer = id1
                    scam = id2
                else:
                    enforcer = id2
                    scam = id1
                try:
                   bot = (await System.get_entity(scam)).bot
                except:
                   bot = False
                await System.gban(enforcer, scam, reason, replied.id, sender, bot=bot)
                orig = re.search(r"t.me/(\w+)/(\d+)", replied.text)
                if orig:
                  await System.send_message(orig.group(1), 'User is a target for enforcement action.\nEnforcement Mode: Lethal Eliminator', reply_to = int(orig.group(2)))

@System.on(system_cmd(pattern=r'reject', allow_inspectors = True, force_reply = True))
async def reject(event):
        #print('Trying OmO')
        replied = await event.get_reply_message()
        me = await System.get_me()
        if replied.from_id == me.id:
            #print('Matching UwU')
            match = re.match(r'\$(SCAN|AUTO(SCAN)?)', replied.text)
            if match:
                #print('Matched OmU')
                id = replied.id
                await System.edit_message(Sibyl_logs, id, reject_string)
        orig = re.search(r"t.me/(\w+)/(\d+)", replied.text)
        _orig = re.search(r"t.me/c/(\w+)/(\d+)", replied.text)
        flags, reason = seprate_flags(event.text)
        if _orig and 'r' in flags.keys():
          await System.send_message(_orig.group(1), 'Crime coefficient less than 100\nUser is not a target for enforcement action\nTrigger of dominator will be locked.', reply_to = int(_orig.group(2)))
        if orig and 'r' in flags.keys():
          await System.send_message(orig.group(1),'Crime coefficient less than 100\nUser is not a target for enforcement action\nTrigger of dominator will be locked.', reply_to=int(orig.group(2)))
help_plus = """
Here is the help for **Main**:

`scan` - Reply to a message WITH reason to send a request to Sibyl for judgement
`approve` - Approve a scan request (Only works in Public Safety Bureau)
`revert or revive or restore` - Ungban ID
`qproof` - Get quick proof from database for given user id
`proof` - Get message from proof id which is at the end of gban msg
`reject` - Reject a scan request

**Notes:**
`/` `?` `.`are supported prefixes.
**Example:** `/addenf` or `?addenf` or `.addenf`
Adding `-f` to a scan will force an approval. (Sibyl Only)
**Note 2:** adding `-o` will gban & fban the original sender.
**Note 3:** Use -u flag with a url to scan the url
**Note 3:** Use -r with reject to reply to message
**Example:** `/scan -f bitcoin spammer`
**Example 2:** `!scan -f -o owo`
Also see "?help extras" for extended functions.
"""

__plugin_name__ = "Main"
