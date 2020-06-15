from telethon import TelegramClient
from .strings import scan_approved_string, bot_gban_string, reject_string, proof_string, forced_scan_string
from Sibyl_System import Sibyl_logs, Sibyl_approved_logs, GBAN_MSG_LOGS, BOT_TOKEN, API_ID_KEY, API_HASH_KEY
from Sibyl_System.plugins.Mongo_DB.gbans import update_gban

class SibylClient(TelegramClient):  
    
    """Custom Telethon client class."""
    def __init__(self, *args, **kwargs):
        """Declare stuff."""
        self.gban_logs = GBAN_MSG_LOGS
        self.approved_logs = Sibyl_approved_logs
        self.log = Sibyl_logs
        self.bot = None
        if BOT_TOKEN:
            self.bot = TelegramClient(
                "SibylSystem",
                api_id=API_ID,
                api_hash=API_HASH
            ).start(bot_token=BOT_TOKEN)
        super().__init__(*args, **kwargs)
    
    async def gban(self, enforcer = None, target=None, reason=None, msg_id=None, approved_by=None, auto=False, bot=False) -> bool:
        """Gbans & Fbans user."""
        if self.gban_logs:
            logs = self.gban_logs
        else:
            logs = self.log
        if not auto:
            await self.send_message(logs, f"/gban [{target}](tg://user?id={target}) {reason} // By {enforcer} | #{msg_id}")
            await self.send_message(logs, f"/fban [{target}](tg://user?id={target}) {reason} // By {enforcer} | #{msg_id}")
        else:
            await self.send_message(logs, f"/gban [{target}](tg://user?id={target}) Auto Gban[${msg_id}] {reason}")
            await self.send_message(logs, f"/fban [{target}](tg://user?id={target}) Auto Gban[${msg_id}] {reason}")
        if bot:
            await self.send_message(Sibyl_approved_logs, bot_gban_string.format(enforcer=enforcer, scam=target, reason = reason))
        else:
            await self.send_message(Sibyl_approved_logs, scan_approved_string.format(enforcer=enforcer, scam=target, reason = reason, proof_id = msg_id))
        if await update_gban(victim = int(target), reason=reason, proof_id=int(msg_id), enforcer=int(enforcer)): 
            return True
        else:
            return False
    
    async def ungban(self, target=None, reason=None) -> bool:
        if self.gban_logs:
            logs = self.gban_logs
        else:
            logs = self.log
        await self.send_message(logs, f'/ungban [{target}](tg://ueser?id={target}) {reason}')
        await self.send_message(logs, f'/unfban [{target}](tg://ueser?id={target}) {reason}')
        if await update_gban(victim = target, reason=reason, proof_id=msg_id, enforcer=enforcer, add=False): 
            return True
        else:
            return False
        
  
  
