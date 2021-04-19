from telethon import events, Button
from uniborg.util import admin_cmd
import time
import os
import random
from stdplugins.sql_helpers.users_sql import get_user, add_user, get_all_users
from stdplugins.sql_helpers.hits_sql import hitExists, addHit, remHit, get_all_hits


channelId = -1001313593468
channelName = "@NordVpn_1"
hitChannelId = -1001296437520
ownerIDs = [630654925, 1111214141]

def genAccount(_list):
    return _list[random.randint(0, len(_list) - 1)]


@borg.on(events.NewMessage(func=lambda e: not e.is_private))
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
        entity = await borg.get_entity(event.chat_id)
        first_name = entity.first_name
        if "/gen" == event.raw_text.lower():
            accounts = get_all_hits()
            if accounts:
                hit = genAccount(accounts).hit.split(":")
                msg = f"""𝙃𝙚𝙧𝙚 𝙄𝙨 𝙔𝙤𝙪𝙧 NordVPN 𝘼𝙘𝙘𝙤𝙪𝙣𝙩

𝙀𝙢𝙖𝙞𝙡: `{hit[0]}`
𝙋𝙖𝙨𝙨: `{hit[1]}`
𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙 𝘽𝙮: **{first_name}**

𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙢𝙚!
❤️𝙎𝙝𝙖𝙧𝙚 & 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 **@nordvpn_1**❤️"""
                await borg.send_message(event.chat_id, msg)
            else:
                await borg.send_message(event.chat_id, "No account available right now.")
        if '/start' == event.raw_text.lower():
            msg = f"""**Hi {first_name},
I am an Account Generator Bot
-------------------------------------------------
I can provide premium accounts of different services
--------------------------------------------------
Do /gen** **to generate an account
--------------------------------------------------
❤️Brought to You By @PandaZnetwork❤️**"""
            await borg.send_message(event.chat_id, msg)
            return
        if '/count' == event.raw_text.lower():
            userList = get_all_users()
            await borg.send_message(event.chat_id, f"{len(userList)} users.")
        if event.chat_id in ownerIDs:
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
                    if not hitExists(hit):
                        addHit(hit)
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
    if event.chat_id == hitChannelId:
        lines = event.raw_text.split("\n")
        if lines[0] == "NordVPN":
            hit = lines[3].split(": ")[1].strip() + ":" + lines[4].split(": ")[1].strip()
            if not hitExists(hit):
                addHit(hit)