from Sibyl_System import SIBYL, ENFORCERS, session
from Sibyl_System import System, system_cmd
import asyncio
from telethon import events
import re 
from telethon.utils import resolve_invite_link

@System.on(system_cmd(pattern=r'addenf'))
async def addenf(event):
     if event.reply:
        replied = await event.get_reply_message()
        id = replied.sender.id
     else:
        id = event.text.split(" ", 2)[1]
     if id in ENFORCERS:
           await System.send_message(event.chat_id, 'That person is already Enforcer!')
           return
     ENFORCERS.append(id)
     await System.send_message(event.chat_id, f'Added [{id}](tg://user?id={id}) to Enforcers') 

@System.on(system_cmd(pattern=r'rmenf'))
async def rmenf(event):
     if event.reply:
        replied = await event.get_reply_message()
        id = replied.sender.id
     else:
        id = event.text.split(" ", 2)[1]
     if id in ENFORCERS:
           ENFORCERS.remove(id)
           await System.send_message(event.chat_id, f'Removed [{id}](tg://user?id={id}) from Enforcers') 
           return
     await System.send_message(event.chat_id, 'Is that person even a Enforcer?') 

@System.on(system_cmd(pattern=r'listenf'))
async def listuser(event):
      msg = "Enforcers:\n"
      for z in ENFORCERS:
         try:
           user = await System.get_entity(z)
           msg += f"•[{user.first_name}](tg://user?id={user.id}) | {z}\n"
         except:
           msg += f"•{z}\n"
      await System.send_message(event.chat_id, msg)

from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest

@System.on(system_cmd(pattern=r'join'))
async def join(event):
      try:
        link = event.text.split(" ", 1)[1]
      except:
        return
      private = re.match(r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org|com)/joinchat/(.*)", link)
      if private:
            await System(ImportChatInviteRequest(private.group(5)))
            await System.send_message(event.chat_id, "Joined chat!")
      else:
          await System(JoinChannelRequest(link))
          await System.send_message(event.chat_id, "Joined chat!") 


@System.on(system_cmd(pattern=r'resolve'))
async def resolve(event):
      try:
        link = event.text.split(" ", 1)[1]
      except:
        return
      match = re.match(r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org)/joinchat/(.*)", link)
      if match:
        try:
           data = resolve_invite_link(match.group(5))
        except:
           await System.send_message(event.chat_id,"Couldn't fetch data from that link") 
           return 
        await System.send_message(event.chat_id, f"Info from hash {match.group(5)}:\n**Link Creator**: {data[0]}\n**Chat ID**: {data[1]}")


@System.on(system_cmd(pattern=r'leave'))
async def leave(event):
      try:
        link = event.text.split(" ", 1)[1]
      except:
        return
      id = re.match('(\d+)', link)
      if id:
         await System(LeaveChannelRequest(int(id.group(0))))
         await System.send_message(event.chat_id, f"Successfully Left chat with id[{id}]") 
      else:
         await System(LeaveChannelRequest(link))
         await System.send_message(event.chat_id, f"Successfully Left chat[{link}]")

@System.on(system_cmd(pattern=r'get_redirect '))
async def redirect(event):
   try:
     url = event.text.split(" ", 1)[1]
   except:
     return
   if not url.startswith('https://') or not url.startswith('http://'):
      url = 'https://' + url 
   async with session.get(url) as r:
       url = r.url
   await System.send_message(event.chat_id, url) 




help_plus = """
Help! 
`addenf` - add a user to enforcers 
Format : addenf <user id / as reply >
`rmenf` - remove a user from enforcers 
Format : rmenf <user id/ as reply>
`listenf` - List all enforcers
`join` - join a chat 
Format : join < chat username or invite link >
`leave` - leave a chat 
Format : leave < chat username or id >
`resolve` - owo
"""

__plugin_name__ = "extras" 
