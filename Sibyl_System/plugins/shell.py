from Sibyl_System import system_cmd, System
import asyncio

@System.on(system_cmd("(term|terminal|sh|shell) "))
async def shell(event):
  if event.fwd_from: return
  cmd = event.text.split(" ", 1)
  if len(cmd) == 1: return
  else: cmd = cmd[1]
  async_process =  await asyncio.create_subprocess_shell(cmd, 
  stdout=asyncio.subprocess.PIPE, 
  stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await async_process.communicate()
  msg = ""
  if stderr.decode(): msg += f"**stderr:**\n`{stderr.decode()}`"
  if stdout.deocde(): msg += f"**stdout:**\n`{stdout.decode()}`"
  await event.reply(msg)

__plugin_name__ = "shell"

help_plus = """
Cmd - sh or shell or term or terminal
Example - `?sh echo owo`
Output - owo
"""
