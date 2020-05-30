on_string = """
**Portable Psychological Diagnosis and Supression System**
Connection successful.
`Dominator` is now active. Cymatic scans are now possible!
"""

# Make sure not to change this too much
# If you still wanna change it change the regex too
scan_request_string = """
$SCAN
Cymatic Scan request
**Enforcer:** {enforcer} 
**User scanned:** {spammer}
**Scan Reason:** `{reason}`
**Chat Originated from:** {chat}
**Target Message:** `{message}`
"""

scan_approved_string = """
#LethalEliminator
**Target User:** `{scam}`
**Crime Coefficient:** `Over 300`
**Reason:** `{reason}`
**Enforcer:** `{enforcer}`
**Case Number:** `{proof_id}`
"""

bot_gban_string = """
#DestroyDecomposer
**Enforcer:** `{enforcer}`
**Target User:** `{scam}`
**Reason:** `{reason}`
"""

# https://psychopass.fandom.com/wiki/Crime_Coefficient_(Index)
# https://psychopass.fandom.com/wiki/The_Dominator
