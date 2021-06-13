from telethon import events, Button
from uniborg.util import admin_cmd
import time
import os
import random
from stdplugins.sql_helpers.users_sql import get_user, add_user, get_all_users, updateLimit, resetDailyLimit, exceededLimitUsers
from stdplugins.sql_helpers.hits_sql import hitExists, addHit, remHit, get_all_hits, get_hit_by_id
import io
import requests
import re
from apscheduler.schedulers.asyncio import AsyncIOScheduler




channelId = -1001313593468
channelName = "@NordVpn_1"
# hitChannelId = -1001296437520
hitChannelId = 0
repotGroupID = -1001206527793
ownerIDs = [630654925, 1111214141]
maintenanceMode = True
dailyLimit = 3
botToken = "1202514912:AAE2yMJiiRTbP2nXYhp2ksHPjJYe5GlVCxo"


reportMsg = """**New Report**

**Hit Details:-**

ID => `{hitID}`
Email => `{email}`
Password => `{pwd}`
Combo=> `{combo}`

**User Details:-**

ID => `{userID}`
First Name => `{first_name}`
Last Name => `{last_name}`
Username => {username}
"""


def genAccount(_list):
    return _list[random.randint(0, len(_list) - 1)]


@borg.on(events.NewMessage(func=lambda e: e.is_private))
async def my_event_handler(event):
    try:
        if not get_user(event.chat_id) and (event.chat_id != channelId or event.chat_id != hitChannelId):
            add_user(event.chat_id)
    except:
        pass
    joinMsg = f"""Hello Dear ❤️

[+] For Using This Bot You must Join Channel {channelName}
[+] If u Left The Channel, Bot won't Work 😒
[+] After Joining Channel, Come Back To Bot And Click On /start"""
    try:
        perm = await borg.get_permissions(channelId, event.chat_id)
    except:
        await borg.send_message(event.chat_id, joinMsg)
        return
    if perm.has_default_permissions or perm.is_admin:
        entity = await borg.get_entity(event.chat_id)
        first_name = entity.first_name
        if "/gen" == event.raw_text.lower():
            if maintenanceMode and event.chat_id not in ownerIDs:
                await borg.send_message(event.chat_id, "Bot is under maintenance.")
                return
            user = get_user(event.chat_id)
            if not user:
                add_user(event.chat_id)
            else:
                if int(user.dailylimit) >= dailyLimit:
                    await borg.send_message(event.chat_id, "Daily limit exceeded.")
                    return
                updateLimit(event.chat_id)
            accounts = get_all_hits()
            if accounts:
                hit = genAccount(accounts)
                hitID = hit.hitID
                hit = hit.hit.split(":")
                msg = f"""𝙃𝙚𝙧𝙚 𝙄𝙨 𝙔𝙤𝙪𝙧 NordVPN 𝘼𝙘𝙘𝙤𝙪𝙣𝙩

𝙀𝙢𝙖𝙞𝙡: `{hit[0]}`
𝙋𝙖𝙨𝙨: `{hit[1]}`
𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙 𝘽𝙮: **{first_name}**

𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙢𝙚!
❤️𝙎𝙝𝙖𝙧𝙚 & 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 **@nordvpn_1**❤️"""
                button = [(Button.inline("Report not working", data=f"report_{hitID}"))]
                await borg.send_message(event.chat_id, msg, buttons = button)
            else:
                await borg.send_message(event.chat_id, "No account available right now.")
        if '/start' == event.raw_text.lower():
            msg = f"""**Hi {first_name},
I am an Account Generator Bot
-------------------------------------------------
I can provide premium accounts of different services
--------------------------------------------------
Do /gen to generate an account
--------------------------------------------------
❤️Brought to You By @PandaZnetwork || Made by @HeisenbergTheDanger❤️**"""
            await borg.send_message(event.chat_id, msg)
            return
        if event.chat_id in ownerIDs:
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
            if '/users' == event.raw_text.lower():
                userList = get_all_users()
                if len(userList) == 0:
                    msg = "No user found"
                else:
                    msg = "**Users:-**\n\n"
                    for user in userList:
                        msg += (f'ID - {user.userId}, Daily limit - {user.dailylimit}/{dailyLimit}\n')
                    msg += f'\n**Total {len(userList)} user.**'
                if len(msg) > 4096:
                    with io.BytesIO(str.encode(msg)) as out_file:
                        out_file.name = "users.txt"
                        await borg.send_file(
                            event.chat_id,
                            out_file,
                            force_document=True,
                            allow_cache=False,
                            caption="List of users."
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
            if '/reset' == event.raw_text.lower():
                await reset() 
                await borg.send_message(event.chat_id, "Done")   
            if '/search' == event.raw_text.lower()[0:7]:
                try:
                    ID = int(event.raw_text.lower()[7:])
                except:
                    await borg.send_message(event.chat_id, "Error")
                    return
                try:
                    entity = await borg.get_entity(ID)
                except:
                    await borg.send_message(event.chat_id, "Not found")
                    return
                msg = ""
                msg += f"First name = {entity.first_name}\n"
                msg += f"Last name = {entity.last_name}\n"
                if entity.username:
                    msg += f"Username = @{entity.username}"
                else:
                    msg += "Username = None"
                await borg.send_message(event.chat_id, msg)
            elif event.raw_text == "/broadcast":
                try:
                    previous_message = await event.get_reply_message()
                    if previous_message.media:
                        await borg.send_message(event.chat_id, "Reply to a text msg")
                        time.sleep(1)
                        await event.delete()
                        return
                    try:
                        msg = previous_message.text
                    except:
                        await borg.send_message(event.chat_id, event.message.id, "Reply to a text msg")
                        time.sleep(1)
                        await event.delete()
                        return
                    userList = get_all_users()
                    if len(userList) == 0:
                        msg = "No user found"
                    else:
                        await borg.send_message(event.chat_id, f"Sending to {len(userList)} users.")
                        err = 0 
                        succ = 0
                        for user in userList:
                            try:
                                await borg.send_message(int(user.userId), msg)
                                succ += 1
                            except Exception as e:
                                err += 1
                                print(e)
                        await borg.send_message(event.chat_id, f"Successfully sent to {succ} users with {err} errors.")
                except Exception as error:
                    await borg.send_message(event.chat_id, "Reply to a text msg")
                    print(error)
        if 'yo' == event.raw_text.lower():
            await event.reply('yo')
            return
    else:
        await borg.send_message(event.chat_id, joinMsg)

async def reset():
    msg = "Limit Has Been Reset , You can Generate Your Accounts Now Now !"
    users = exceededLimitUsers(dailyLimit)
    for user in users:
        try:
            await borg.send_message(int(user.userId), msg)
        except Exception as e:
            print(e)
    msg = "Bot reseted."
    url = f"https://api.telegram.org/bot{botToken}/sendMessage?chat_id={ownerIDs[0]}&text={msg}"
    resetDailyLimit()
    requests.get(url)




@borg.on(events.callbackquery.CallbackQuery(data=re.compile(b"report_(.*)")))
async def genAcc(event):
    hitID = event.data_match.group(1).decode("UTF-8")
    hit = get_hit_by_id(hitID)
    email, pwd = hit.hit.split(":", maxsplit = 2)
    entity = await borg.get_entity(event.chat_id)
    username = entity.username
    if username:
        username = "@" + username
    msg = reportMsg.format(
        hitID = hitID,
        email = email,
        pwd = pwd,
        combo = hit.hit,
        userID = event.chat_id,
        first_name = entity.first_name,
        last_name = entity.last_name,
        username = username
    )
    button = [(Button.inline("Remove Now.", data=f"remove_{hitID}"))]
    if repotGroupID:
        await borg.send_message(repotGroupID, msg, buttons=button)
    else:
        await borg.send_message(ownerIDs[0], msg, buttons=button)
    await event.answer("Report Sent to Admins!", alert=True)

@borg.on(events.NewMessage)
async def my_event_handler(event):
    if hitChannelId and event.chat_id == hitChannelId:
        lines = event.raw_text.split("\n")
        if lines[0] == "NordVPN":
            hit = lines[3].split(": ")[1].strip() + ":" + lines[4].split(": ")[1].strip()
            if not hitExists(hit):
                addHit(hit)





scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(reset, 'cron', hour=0)
scheduler.start()
