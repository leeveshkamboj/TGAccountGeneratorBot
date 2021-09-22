import os

class Var(object):
    api_id = os.environ.get("API_ID", None)
    api_hash = os.environ.get("API_HASH", None)
    token = os.environ.get("TOKEN", None)
    ownerIDs = os.environ.get("OWNER_IDS", [])
    if ownerIDs:
        ownerIDs = [int(ID) for ID in ownerIDs.split("|")]
    account_name = os.environ.get("ACCOUNT_NAME", "")
    channelId = int(os.environ.get("CHANNEL_ID", 0))
    channelName = os.environ.get("CHANNEL_NAME", '')
    reportGroupId = int(os.environ.get("REPORT_GROUP_ID", 0))
    dailyLimit = int(os.environ.get("DAILY_LIMIT", 3))
    maintenanceMode = os.environ.get("MAINTENANCE_MODE", False)
    maintenanceMode = True if maintenanceMode == "TRUE" else False