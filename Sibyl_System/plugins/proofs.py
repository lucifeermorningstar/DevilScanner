from Sibyl_System import System, system_cmd

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
