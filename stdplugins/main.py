from telethon import events, Button
from uniborg.util import admin_cmd
import time
import os
import random
from stdplugins.sql_helpers.users_sql import get_user, add_user, get_all_users
from stdplugins.sql_helpers.hits_sql import hitExists, addHit, remHit, get_all_hits


# accounts = ["1test@gmail.com:123", "2test@gmail.com:123523", "3test@gmail.com:asdgah", "4test@gmail.com:sadgd","5test@gmail.com:ssdadfh"]
channelId = -1001313593468
channelName = "@NordVpn_1"
hitChannelId = -1001296437520

def genAccount(_list):
    return _list[random.randint(0, len(_list) - 1)]


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
            accounts = get_all_hits()
            if accounts:
                await borg.send_message(event.chat_id, genAccount(accounts).hit)
            else:
                await borg.send_message(event.chat_id, "No hits found")
        if '/start' == event.raw_text.lower():
            await borg.send_message(event.chat_id, "**Hi**\nUse /gen to geneate account")
            return
        if '/count' == event.raw_text.lower():
            userList = get_all_users()
            await borg.send_message(event.chat_id, f"{len(userList)} users.")
        if '/hits' == event.raw_text.lower():
            hitList = get_all_hits()
            if len(hitList) == 0:
                msg = "Database is empty."
            else:
                msg = "**Hits:-**\n\n"
                for hit in hitList:
                    msg += (f'{hit.hit}\n')
                msg += f'\n**Total {len(hitList)} hits.**'
            if len(msg) > 4096:
                with io.BytesIO(str.encode(msg)) as out_file:
                    out_file.name = "hits.txt"
                    await borg.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="List of hits."
                    )
                return
            else:
                await borg.send_message(event.chat_id, msg)
                return
        if '/addhit' == event.raw_text.lower()[0:7]:
            hits = event.raw_text.lower()[8:].split("\n")
            for hit in hits:
                addHit(hit.strip())
            await borg.send_message(event.chat_id, f"{len(hits)} Hit(s) added.")
        if '/cleanhits' == event.raw_text.lower():
            hitList = get_all_hits()
            for hit in hitList:
                try:
                    remHit(hit.hit)
                except:
                    pass
            await borg.send_message(event.chat_id, "Cleaned...")
        if 'yo' == event.raw_text.lower():
            await event.reply('yo')
            return
    else:
        await borg.send_message(event.chat_id, joinMsg)



@borg.on(events.NewMessage)
async def my_event_handler(event):
    print(event.chat_id)
    if event.chat_id == hitChannelId:
        print(event.raw_text)