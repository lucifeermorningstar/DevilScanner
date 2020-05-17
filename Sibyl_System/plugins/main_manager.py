from Sibyl_System import Sibyl_logs, ENFORCERS, SIBYL, INSPECTORS, Sibyl_approved_logs, GBAN_MSG_LOGS
from Sibyl_System.strings import scan_request_string, scan_approved_string, bot_gban_string
from Sibyl_System import System, system_cmd
from telethon import events
import re
from Sibyl_System import session
import logging


async def gban(enforcer=None, target=None, reason=None, msg_id=None, approved_by=None, auto=False, bot=False):
    """Gbans & Fbans user."""
    if GBAN_MSG_LOGS:
        logs = GBAN_MSG_LOGS
    else:
        logs = Sibyl_logs
    if not auto:
        await System.send_message(logs, f"/gban [{target}](tg://user?id={target}) {reason} // By {enforcer} | #{msg_id}")
        await System.send_message(logs, f"/fban [{target}](tg://user?id={target}) {reason} // By {enforcer} | #{msg_id}")
    else:
        await System.send_message(logs, f"/gban [{target}](tg://user?id={target}) AUTO GBAN | #{msg_id}")
        await System.send_message(logs, f"/fban [{target}](tg://user?id={target}) AUTO GBAN | #{msg_id}")
    if bot:
        await System.send_message(Sibyl_approved_logs, bot_gban_string.format(enforcer=enforcer, scam=target, reason = reason))
    else:
        await System.send_message(Sibyl_approved_logs, scan_approved_string.format(enforcer=enforcer, scam=target, reason = reason, proof_id = msg_id))
    return True

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)


@System.on(system_cmd(pattern=r'scan ', allow_enforcer = True, force_reply = True))
async def scan(event):
        trim = None
        replied = await event.get_reply_message()
        if re.match('.scan -f -o .*',
                    event.text) or re.match(".scan -o .*", event.text):
            if replied.fwd_from:
                if re.match('.scan -o .*', event.text): trim = 2
                else: trim = 3
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
        try:
            if re.match('.scan -f .*', event.text) and executer.id in INSPECTORS:
                if not trim:
                    reason = event.text.split(" ", 2)[2]
                approve = True
            else:
                reason = event.text.split(" ", 1)[1]
                approve = False
        except BaseException:
            return
        if replied.video or replied.document or replied.contact or replied.gif or replied.sticker:
            await replied.forward_to(Sibyl_logs)
        if trim:
            reason = event.text.split(" ", trim)[trim]
        msg = await System.send_message(Sibyl_logs, scan_request_string.format(enforcer=f"[{executer.first_name}](tg://user?id={executer.id})", spammer=sender, chat = f"t.me/{event.chat.username}/{event.message.id}" if event.chat.username else "Occurred in Private Chat - {event.chat.title}", message=replied.text, reason=reason))
        if approve:
            await gban(executer.id, target, reason, msg.id, executer)

@System.on(system_cmd(pattern=r're(vive|vert|store) '))
async def revive(event):
   try:
     user_id = event.text.split(" ", 1)[1]
   except IndexError: return
   a = await event.reply("Casting magic spells to revive the dead person")
   if GBAN_MSG_LOGS:
        logs = GBAN_MSG_LOGS
   else:
        logs = Sibyl_logs
   await System.send_message(logs, f'/ungban {user_id}')
   await System.send_message(logs, f'/unfban {user_id}')
   await a.edit("OwO, It worked") 


@System.on(system_cmd(pattern=r'approve', allow_inspectors=True, force_reply = True))
async def approve(event):
        replied = await event.get_reply_message()
        match = re.match(r'\$SCAN', replied.text)
        auto_match = re.match(r'\$AUTO', replied.text)
        me = await System.get_me()
        if auto_match:
            if replied.sender.id == me.id:
                id = re.search(
                    r"Triggered by: (\[\w+\]\(tg://user\?id=(\d+)\)|(\d+))",
                    replied.text).group(2)
                try:
                     bot = (await System.get_entity(id)).bot
                except:
                     bot = False
                await gban(enforcer=me.id, target=id, msg_id=replied.id, auto=True, bot=bot)
                return "OwO"
        if match:
            reply = replied.sender.id
            sender = await event.get_sender()
            # checks to not gban the Gbanner and find who is who
            if reply == me.id:
                list = re.findall(r'tg://user\?id=(\d+)', replied.text)
                reason = re.search(r"Scan Reason: (.*)", replied.text).group(1)
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
                await gban(enforcer, scam, reason, replied.id, sender, bot=bot)

proof_string = """
**Proof from ID** - {proof_id} :
┣━**Reason**: {reason}
┗━**Message**
         ┣━[Nekobin]({paste})
         ┗━[DelDog]({url})"""

@System.on(events.NewMessage(pattern=r'[\.\?!/]proof'))
async def proof(event):
    if event.from_id in SIBYL:
        msg = await System.send_message(event.chat_id, 'Trying to get Proof owo >>>>>')
        try:
            proof_id = int(event.text.split(' ', 1)[1])
        except BaseException:
            await msg.edit('>>>>> Proof id is not valid')
            return
        await msg.edit('Fetching msg details from proof id <<<<<<<')
        proof = await System.get_messages(Sibyl_logs, ids=proof_id)
        try:
            reason = re.search(r"Scan Reason: (.*)", proof.message).group(1)
        except BaseException:
            await msg.edit('>>>>It looks like I cannot see the msg or the proof id is not valid')
            return
        try:
            message = re.search(
                'Target Message: (.*)',
                proof.message,
                re.DOTALL).group(1)
        except BaseException:
                proof_id -= 1
                proof = await System.get_messages(Sibyl_logs, ids=proof_id)
                if proof:
                    if proof.media:
                        await msg.edit('Proof is media -> Forwarding message') 
                        await proof.forward_to(event.chat_id)
                        return
                    else:
                        await msg.edit(f"Error getting proof from id {proof_id}")
                        return
                else:
                    await msg.edit(f" Failed to get proof, Is the proof id valid?")
                    return
        async with session.post('https://nekobin.com/api/documents', json={'content': message}) as r:
            paste = f"https://nekobin.com/{(await r.json())['result']['key']}"
        url = "https://del.dog/documents"
        async with session.post(url, data=message.encode("UTF-8")) as f:
             r = await f.json()
             url = f"https://del.dog/{r['key']}"
        await msg.edit(proof_string.format(proof_id = proof_id, reason=reason, paste=paste, url=url))

reject_string = """
$REJECTED
**Crime Coefficient**: `Under 100`

Target is not a target for enforcement action. The trigger of Dominator will be locked.
"""


@System.on(system_cmd(pattern=r'reject', allow_inspectors = True, force_reply = True))
async def reject(event):
        #print('Trying OmO')
        replied = await event.get_reply_message()
        me = await System.get_me()
        if replied.from_id == me.id:
            #print('Matching UwU')
            match = re.match(r'\$SCAN', replied.text)
            if match:
                #print('Matched OmU')
                id = replied.id
                await System.edit_message(Sibyl_logs, id, reject_string)

help_plus = """
Here is the help for **Main**:

`scan` - **Reply to a message WITH reason to send a request to Sibyl for judgement**
`approve` - **Approve a scan request (Only works in Public Safety Bureau)**
`revert or revive or restore` - **Ungban ID**
`proof` - **Get message from proof id which is at the end of gban msg **
`reject` - **Reject a scan request**

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
