from telethon import events, Button
from uniborg.util import admin_cmd
import time
import os
import random

accounts = ["1test@gmail.com:123", "2test@gmail.com:123523", "3test@gmail.com:asdgah", "4test@gmail.com:sadgd","5test@gmail.com:ssdadfh"]
channelId = -1001313593468
channelName = "@NordVpn_1"

def genAccount(list):
    return list[random.randint(0, len(accounts) - 1)]


@borg.on(events.NewMessage)
async def my_event_handler(event):
    try:
        if not get_user(event.chat_id):
            add_user(event.chat_id)
    except:
        pass
    joinMsg = f"Please Join {channelName} to use this bot."
    try:
        perm = await borg.get_permissions(channelId, event.chat_id)
    except:
        await borg.send_message(event.chat_id, joinMsg)
        return
    if perm.has_default_permissions or perm.is_admin:
        if "/gen" == event.raw_text.lower():
            await borg.send_message(event.chat_id, genAccount(accounts))
        if '/start' == event.raw_text.lower():
            await borg.send_message(event.chat_id, "**Hi**\nUse /gen to geneate account")
            return
        if '/count' == event.raw_text.lower():
            userList = get_all_users()
            await borg.send_message(event.chat_id, f"{len(userList)} users.")
        if 'yo' == event.raw_text.lower():
            await event.reply('yo')
            return
    else:
        await borg.send_message(event.chat_id, joinMsg)