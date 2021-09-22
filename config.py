import os

class Var(object):
    ownerIDs = os.environ.get("OWNER_IDS", [])
    if ownerIDs:
        ids = ownerIDs.split("|")
        ownerIDs = [int(ID) for ID in ids]
    channelId = int(os.environ.get("CHANNEL_ID", 0))
    groupId = int(os.environ.get("GROUP_ID", 0))
    repotGroupId = int(os.environ.get("REPORT_GROUP_ID", 0))
    channelName = os.environ.get("CHANNEL_NAME", '')
    hitChannelId = int(os.environ.get("HIT_CHANNEL_ID", 0))
    dailyLimit = int(os.environ.get("DAILY_LIMIT", 3))
    maintenanceMode = os.environ.get("MAINTENANCE_MODE", False)
    if maintenanceMode == "TRUE":
        maintenanceMode = True
    else:
        maintenanceMode = False