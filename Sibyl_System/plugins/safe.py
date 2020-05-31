from Sibyl_System import System, system_cmd
import os
import sys

@System.on(system_cmd(pattern = r"sibyl restart"))
async def reboot(event):
    if event.fwd_from:
        return
    await event.reply('Restarting.....')
    await System.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@System.on(system_cmd(pattern = r"sibyl shutdown"))
async def shutdown(event):
    if event.fwd_from:
        return
    await event.reply("Shutting Down... ")
    await System.disconnect()
