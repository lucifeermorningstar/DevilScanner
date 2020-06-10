from Sibyl_System import Sibyl_logs, ENFORCERS, SIBYL, INSPECTORS, GBAN_MSG_LOGS
from Sibyl_System.strings import scan_request_string, scan_approved_string, bot_gban_string, reject_string, proof_string, forced_scan_string
from Sibyl_System import System, system_cmd
import re
from Sibyl_System import session
import Sibyl_System.plugins.Mongo_DB.gbans as db
import logging


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)


@System.on(system_cmd(pattern=r'scan ', allow_enforcer = True, force_reply = True))
async def scan(event):
        trim = None
        replied = await event.get_reply_message()
        if re.match('.scan (-f )?-o .*', event.text) 
        or re.match(".scan -o .*", event.text) 
        or re.match(".scan (-f )?-p", event.text):
            if replied.fwd_from:
                if re.match('.scan -o .*', event.text): trim = 2
                elif: trim = 3
                reply = replied.fwd_from
                target = reply.from_id
                if reply.from_id in ENFORCERS or reply.from_id in SIBYL:
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
        try:
            if re.match('.scan -f .*', event.text) and executer.id in INSPECTORS:
                if not trim:
                    reason = event.text.split(" ", 2)[2]
                approve = True
            else:
                reason = event.text.split(" ", 1)[1]
                approve = False
            match = re.match('.scan -f -p (\d+) .*', event.text)
            if  match and executer.id in INSPECTORS:
                rep_proof = True
                req_user = match.group(1)
        except BaseException:
            return
        if replied.video or replied.document or replied.contact or replied.gif or replied.sticker:
            await replied.forward_to(Sibyl_logs)
        if trim:
            reason = event.text.split(" ", trim)[trim]
        executor = f'[{executer.first_name}](tg://user?id={executer.id})'
        chat = f"t.me/{event.chat.username}/{event.message.id}" if event.chat.username else f"Occurred in Private Chat - {event.chat.title}"
        await event.reply("Scanning.")
        if req_proof and req_user:
          await replied.forward_to(Sibyl_logs)
          await System.gban(executer.id, req_user, reason, msg.id, executer)
        if not approve:
           msg = await System.send_message(Sibyl_logs, scan_request_string.format(enforcer=executor, spammer=sender, chat=chat , message=replied.text, reason=reason))
        if approve:
           msg = await System.send_message(Sibyl_logs, forced_scan_string.format(ins = executor, spammer=sender, chat=chat,message=replied.text, reason=reason))
           await System.gban(executer.id, target, reason, msg.id, executer)

@System.on(system_cmd(pattern=r're(vive|vert|store) '))
async def revive(event):
   try:
     user_id = event.text.split(" ", 1)[1]
   except IndexError: return
   a = await event.reply("Casting magic spells to revive the dead person")
   await System.ungban(user_id, f" By //{(await event.get_sender()).id}")
   await a.edit("OwO, It worked")


@System.on(system_cmd(pattern=r'approve', allow_inspectors=True, force_reply = True))
async def approve(event):
        replied = await event.get_reply_message()
        match = re.match(r'\$SCAN', replied.text)
        auto_match = re.match(r'\$AUTO(SCAN)?', replied.text)
        me = await System.get_me()
        if auto_match:
            if replied.sender.id == me.id:
                id = re.search(
                    r"Scanned user: (\[\w+\]\(tg://user\?id=(\d+)\)|(\d+))",
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
                  await System.send_message(orig.group(1), 'Scan approved, Taking action...', reply_to = int(orig.group(2)))

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

@System.on(system_cmd(pattern=r'qproof ', allow_inspectors=True))
async def qproof(event):
   user = event.text.split(' ', 1)
   if len(user) == 1: return
   user_data = await db.get_gban(int(user[1]))
   if not user_data:
        await event.reply('User is not gbanned')
        return
   message = f"User: {user_data['user']}\n"\
                       f"Enforcer: {user_data['enforcer']}\n"\
                       f"Reason: {user_data['reason']}\n"\
                       f"Extended Proof: {user_data['proof_id']}"
   await event.reply(message)
      




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
        if orig:
          await System.send_message(orig.group(1),'Scan rejected.', reply_to=int(orig.group(2)))

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
**Note 2:** adding `-o` will gban & fban the original sender, If using both approve and original sender flag the "-f" flag must come first!
**Example:** `/scan -f bitcoin spammer`
**Example 2:** `!scan -f -o owo`
Also see "?help extras" for extended functions.
"""

__plugin_name__ = "Main"
