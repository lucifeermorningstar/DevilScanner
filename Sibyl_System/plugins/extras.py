from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from Sibyl_System import ENFORCERS, session
from Sibyl_System import System, system_cmd
import re
from telethon.utils import resolve_invite_link
import heroku3
import os 

try:
    from Sibyl_System import HEROKU_API_KEY, HEROKU_APP_NAME
    heroku_conn = heroku3.from_key(HEROKU_API_KEY)
    app = heroku_conn.app(HEROKU_APP_NAME)
    config = app.config()
    HEROKU = True
except BaseException:
    HEROKU = False


@System.on(system_cmd(pattern=r'addenf'))
async def addenf(event) -> None:
    if event.reply:
        replied = await event.get_reply_message()
        u_id = replied.sender.id
    else:
        u_id = event.text.split(" ", 2)[1]
    if u_id in ENFORCERS:
        await System.send_message(event.chat_id, 'That person is already Enforcer!')
        return
    if HEROKU:
        config['ENFORCERS'] = os.environ.get('ENFORCERS') + ' ' + str(u_id)
    else:
        ENFORCERS.append(u_id)
    await System.send_message(event.chat_id, f'Added [{u_id}](tg://user?id={u_id}) to Enforcers')


@System.on(system_cmd(pattern=r'rmenf'))
async def rmenf(event) -> None:
    if event.reply:
        replied = await event.get_reply_message()
        u_id = replied.sender.id
    else:
        u_id = event.text.split(" ", 2)[1]
    if u_id not in ENFORCERS:
        await System.send_message(event.chat_id, 'Is that person even a Enforcer?')
        return
    if HEROKU:
        config['ENFORCERS'] = os.environ.get('ENFORCERS').strip(u_id)
    else:
        ENFORCERS.remove(u_id)
    await System.send_message(event.chat_id, f'Removed [{u_id}](tg://user?id={u_id}) from Enforcers')




@System.on(system_cmd(pattern=r'enforcers'))
async def listuser(event) -> None:
    msg = "Enforcers:\n"
    for z in ENFORCERS:
        try:
            user = await System.get_entity(z)
            msg += f"•[{user.first_name}](tg://user?id={user.id}) | {z}\n"
        except BaseException:
            msg += f"•{z}\n"
    await System.send_message(event.chat_id, msg)


@System.on(system_cmd(pattern=r'join'))
async def join(event) -> None:
    try:
        link = event.text.split(" ", 1)[1]
    except BaseException:
        return
    private = re.match(
        r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org)/joinchat/(.*)",
        link)
    if private:
        await System(ImportChatInviteRequest(private.group(5)))
        await System.send_message(event.chat_id, "Joined chat!")
    else:
        await System(JoinChannelRequest(link))
        await System.send_message(event.chat_id, "Joined chat!")


@System.on(system_cmd(pattern=r'resolve'))
async def resolve(event) -> None:
    try:
        link = event.text.split(" ", 1)[1]
    except BaseException:
        return
    match = re.match(
        r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org)/joinchat/(.*)",
        link)
    if match:
        try:
            data = resolve_invite_link(match.group(5))
        except BaseException:
            await System.send_message(event.chat_id, "Couldn't fetch data from that link")
            return
        await System.send_message(event.chat_id, f"Info from hash {match.group(5)}:\n**Link Creator**: {data[0]}\n**Chat ID**: {data[1]}")


@System.on(system_cmd(pattern=r'leave'))
async def leave(event) -> None:
    try:
        link = event.text.split(" ", 1)[1]
    except BaseException:
        return
    c_id = re.match(r'-(\d+)', link)
    if c_id:
        await System(LeaveChannelRequest(int(c_id.group(0))))
        await System.send_message(event.chat_id, f"Successfully Left chat with id[{c_id}]")
    else:
        await System(LeaveChannelRequest(link))
        await System.send_message(event.chat_id, f"Successfully Left chat[{link}]")


@System.on(system_cmd(pattern=r'get_redirect '))
async def redirect(event) -> None:
    try:
        of = event.text.split(" ", 1)[1]
    except BaseException:
        return
    if not url.startswith('https://') or not url.startswith('http://'):
        of = 'https://' + of
    async with session.get(of) as r:
        url = r.url
    await System.send_message(event.chat_id, url)


help_plus = """
Help!
`addenf` - Adds a user as an enforcer.
Format : addenf <user id / as reply >
`rmenf` - Removes a user from enforcers.
Format : rmenf <user id/ as reply>
`enforcers` - Lists all enforcers.
`join` - Joins a chat.
Format : Joins < chat username or invite link >
`leave` - Leaves a chat.
Format : Leaves < chat username or id >
`resolve` - owo
`get_redirect` - get redirect of a link
**Notes:**
`/` `?` `.` `!` are supported prefixes.
**Example:** `/addenf` or `?addenf` or `.addenf`
"""

__plugin_name__ = "extras"
