on_string = """
**Portable Psychological Diagnosis and Supression System**
Connection to Sibyl System was successful.
`Dominator` is now active. Cymatic scans are now possible!
"""

# Make sure not to change this too much
# If you still wanna change it change the regex too
scan_request_string = """
$SCAN
{enforcer} is requesting a Cymatic Scan for {spammer}
**Scan Reason:** `{reason}`
**Target Message:** `{message}`
**Chat Originated from:** {chat}
"""

scan_approved_string = """
#LETHAL_ELIMINATOR
**Target User:** `{scam}`
**Crime Coefficient:** `Over 300`
**Reason:** `{reason}`
**Enforcer:** `{enforcer}`
**Case Number:** `{proof_id}`
"""

bot_gban_string = """
#DESTROY_DECOMPOSER
**Enforcer:** `{enforcer}`
**Target User:** `{scam}`
**Reason:** `{reason}`
"""

# https://psychopass.fandom.com/wiki/Crime_Coefficient_(Index)
# https://psychopass.fandom.com/wiki/The_Dominator
