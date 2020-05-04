from Sibyl_System import System, system_cmd
from Sibyl_System.strings import on_string
import logging
import importlib

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

from Sibyl_System.plugins import to_load

HELP = {}
IMPORTED = {}

for load in to_load:
    imported = importlib.import_module("Sibyl_System.plugins." + load)
    if not hasattr(imported, "__plugin_name__"):
        imported.__plugin_name__ = imported.__name__

    if not imported.__plugin_name__.lower() in IMPORTED:
        IMPORTED[imported.__plugin_name__.lower()] = imported

    if hasattr(imported, "help_plus") and imported.help_plus:
        HELP[imported.__plugin_name__.lower()] = imported

@System.on(system_cmd(pattern=r'status'))
async def status(event):
         await event.reply(on_string)

@System.on(system_cmd(pattern=r'help', allow_slash=False))
async def send_help(event):
         try:
            help_for = event.text.split(" ", 1)[1].lower()
         except IndexError:
            msg = "Here is the list of plugins with Help text:\n"
            for x in HELP.keys():
                msg += f"`{x.capitalize()}`\n"
            await event.reply(msg)
            return
         if help_for in HELP:
              await event.reply(HELP[help_for].help_plus)
         else:
              return


System.start()
System.run_until_disconnected()
