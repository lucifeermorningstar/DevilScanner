from telethon import TelegramClient
from Sibyl_System.strings import scan_request_string, scan_approved_string, bot_gban_string, reject_string, proof_string, forced_scan_string
from Sibyl_System import Sibyl_logs, Sibyl_approved_logs, GBAN_MSG_LOGS

class SibylClient(TelegramClient):
    """Custom Telethon client class."""

    self.gban_logs = GBAN_MSG_LOGS
    self.approved_logs = Sibyl_approved_logs
    self.log = Sibyl_logs
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def gban(enforcer = None, target=None, reason=None, msg_id=None, approved_by=None, auto=False, bot=False) -> bool:
        """Gbans & Fbans user."""
        if self.gban_logs:
            logs = self.gban_logs
        else:
            logs = self.log
        if not auto:
            await self.send_message(logs, f"/gban [{target}](tg://user?id={target}) {reason} // By {enforcer} | #{msg_id}")
            await self.send_message(logs, f"/fban [{target}](tg://user?id={target}) {reason} // By {enforcer} | #{msg_id}")
        else:
            await self.send_message(logs, f"/gban [{target}](tg://user?id={target}) Auto Gban[${msg_id}]")
            await self.send_message(logs, f"/fban [{target}](tg://user?id={target}) Auto Gban[${msg_id}]")
        if bot:
            await self.send_message(Sibyl_approved_logs, bot_gban_string.format(enforcer=enforcer, scam=target, reason = reason))
        else:
            await self.send_message(Sibyl_approved_logs, scan_approved_string.format(enforcer=enforcer, scam=target, reason = reason, proof_id = msg_id))
        return True
        
  
  
