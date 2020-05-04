"""Gets ENV vars or Config vars then makes Telethon client."""
from telethon import TelegramClient, events
import aiohttp
from telethon.sessions import StringSession
import os
import pymongo
import re


ENV = bool(os.environ.get('ENV', False))
if ENV:
    API_ID_KEY = int(os.environ.get('API_ID_KEY', None))
    API_HASH_KEY = os.environ.get('API_HASH_KEY', None)
    STRING_SESSION = os.environ.get('STRING_SESSION', None)
    HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY', None)
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
    RAW_SIBYL = os.environ.get("SIBYL", "")
    RAW_ENFORCERS = os.environ.get("ENFORCERS", "")
    SIBYL = list(int(x) for x in os.environ.get("SIBYL", "").split())
    INSPECTORS = list(int(x) for x in os.environ.get("INSPECTORS", "").split())
    ENFORCERS = list(int(x) for x in os.environ.get("ENFORCERS", "").split())
    MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
    Sibyl_logs = int(os.environ.get('Sibyl_logs', None))
    Sibyl_approved_logs = int(os.environ.get('Sibyl_Approved_Logs', None))
    GBAN_MSG_LOGS = int(os.environ.get('GBAN_MSG_LOGS', None))
else:
    import Sibyl_System.config as Config
    API_ID_KEY = Config.API_ID
    API_HASH_KEY = Config.API_HASH
    STRING_SESSION = Config.STRING_SESSION
    MONGO_DB_URL = Config.MONGO_DB_URL
    SIBYL = Config.SIBYL
    ENFORCERS = Config.ENFORCERS
    INSPECTORS = Config.INSPECTORS
    Sibyl_logs = Config.Sibyl_logs
    Sibyl_approved_logs = Config.Sibyl_approved_logs
    GBAN_MSG_LOGS = Config.GBAN_MSG_LOGS

ENFORCERS.extend(SIBYL)
session = aiohttp.ClientSession()
System = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID_KEY,
    API_HASH_KEY)
MONGO_CLIENT = pymongo.MongoClient(MONGO_DB_URL)
collection = MONGO_CLIENT['Sibyl']['Main']
if collection.count_documents({'_id': 1}, limit=1) == 0:
    dictw = {"_id": 1}
    dictw["blacklisted"] = []
    collection.insert_one(dictw)

if collection.count_documents({'_id': 2}, limit=1) == 0:
    dictw = {"_id": 2, "Type": "Wlc Blacklist"}
    dictw["blacklisted_wlc"] = []
    collection.insert_one(dictw)


def system_cmd(pattern=None, allow_sibyl=True,
               allow_enforcer=False, allow_inspectors = True, allow_slash=True, **args):
    if pattern and allow_slash:
        args["pattern"] = re.compile(r"[\?\.!/]" + pattern)
    else:
        args["pattern"] = re.compile(r"[\?\.!]" + pattern)
    if allow_sibyl and allow_enforcer:
        args["from_users"] = ENFORCERS
    elif allow_inspectors and allow_sibyl:
        args["from_users"] = INSPECTORS
    else:
        args["from_users"] = SIBYL
    return events.NewMessage(**args)
