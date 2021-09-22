from telethon.sync import TelegramClient
from telethon import events, Button
from config import Var
import time
import os
import random
from stdplugins.sql_helpers.users_sql import get_user, add_user, remUser, get_all_users, updateLimit, resetDailyLimit, exceededLimitUsers
from stdplugins.sql_helpers.hits_sql import hitExists, addHit, remHit, get_all_hits, get_hit_by_id
import io
import requests
import re
from apscheduler.schedulers.asyncio import AsyncIOScheduler


####################################################################

bot = TelegramClient('bot', Var.api_id, Var.api_hash).start(bot_token=Var.token)

####################################################################

joinMsg = """Hello Dear ❤️

[+] For Using This Bot You must Join Channel {channelName}
[+] If u Left The Channel, Bot won't Work 😒
[+] After Joining Channel, Come Back To Bot And Click On /start"""


genMsg = """𝙃𝙚𝙧𝙚 𝙄𝙨 𝙔𝙤𝙪𝙧 {account} 𝘼𝙘𝙘𝙤𝙪𝙣𝙩

𝙀𝙢𝙖𝙞𝙡: `{email}`
𝙋𝙖𝙨𝙨: `{pwd}`
𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙 𝘽𝙮: **{name}**

𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙢𝙚!
❤️𝙎𝙝𝙖𝙧𝙚 & 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 **{channelName}**❤️"""


####################################################################

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
Daily Limit => {dailyLimit}/{TotalDailyLimit}
"""

####################################################################

startMsg = """**Hi {name},
I am an Account Generator Bot
-------------------------------------------------
I can provide premium accounts of different services
--------------------------------------------------
Do /gen to generate an account
--------------------------------------------------
❤️Brought to You By @PandaZnetwork || Made by @HeisenbergTheDanger❤️**"""

####################################################################


@bot.on(events.NewMessage(func=lambda e: e.is_private))
async def my_event_handler(event):
    try:
        if not get_user(event.chat_id) and event.chat_id != Var.channelId:
            add_user(event.chat_id)
    except:
        pass
    try:
        perm = await bot.get_permissions(Var.channelId, event.chat_id)
    except:
        await bot.send_message(event.chat_id, joinMsg.format(channelName = Var.channelName))
        return
    if not (perm.has_default_permissions or perm.is_admin):
        await bot.send_message(event.chat_id, joinMsg.format(channelName = Var.channelName))
        return
    entity = await bot.get_entity(event.chat_id)
    first_name = entity.first_name
    if "/gen" == event.raw_text.lower():
        if Var.maintenanceMode and event.chat_id not in Var.ownerIDs:
            await bot.send_message(event.chat_id, "Bot is under maintenance.")
            return
        user = get_user(event.chat_id)
        if not user:
            add_user(event.chat_id)
        else:
            if int(user.dailylimit) >= Var.dailyLimit and event.chat_id not in Var.ownerIDs:
                await bot.send_message(event.chat_id, "Daily limit exceeded.")
                return
            elif int(user.dailylimit) != Var.dailyLimit:
                updateLimit(event.chat_id)
        accounts = get_all_hits()
        if accounts:
            hit = random.choices(accounts)
            print(hit)
            hitID = hit.hitID
            hit = hit.hit.split(":")
            
            button = [
                [Button.url("Authentication error?", "https://t.me/nordbypass")],
                [(Button.inline("Report not working", data=f"report_{hitID}"))]
            ]
            await bot.send_message(event.chat_id, genMsg.format(account = Var.account_name, email = hit[0], pwd = hit[1], name = first_name, channelName = Var.channelName), buttons = button)
        else:
            await bot.send_message(event.chat_id, "No account available right now.")
    if '/start' == event.raw_text.lower():
        await bot.send_message(event.chat_id, startMsg.format(name = first_name))
        return
    if event.chat_id in Var.ownerIDs:
        if '/count' == event.raw_text.lower():
            userList = get_all_users()
            await bot.send_message(event.chat_id, f"{len(userList)} users.")
        if '/hits' == event.raw_text.lower():
            hitList = get_all_hits()
            if len(hitList) == 0:
                msg = "Database is empty."
            else:
                msg = "**Hits-**\n\n"
                for hit in hitList:
                    msg += (f'{hit.hit}\n')
                msg += f'\n**Total {len(hitList)} hits.**'
            if len(msg) > 4096:
                with io.BytesIO(str.encode(msg)) as out_file:
                    out_file.name = "hits.txt"
                    await bot.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="List of hits."
                    )
                return
            else:
                await bot.send_message(event.chat_id, msg)
                return
        if '/users' == event.raw_text.lower():
            userList = get_all_users()
            if len(userList) == 0:
                msg = "No user found"
            else:
                msg = "**Users:-**\n\n"
                for user in userList:
                    msg += (f'ID - {user.userId}, Daily limit - {user.dailylimit}/{Var.dailyLimit}\n')
                msg += f'\n**Total {len(userList)} user.**'
            if len(msg) > 4096:
                with io.BytesIO(str.encode(msg)) as out_file:
                    out_file.name = "users.txt"
                    await bot.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="List of users."
                    )
                return
            else:
                await bot.send_message(event.chat_id, msg)
                return
        if '/addhits' == event.raw_text.lower():
            if event.is_reply:
                try:
                    previous_message = await event.get_reply_message()
                    response = previous_message
                except:
                    pass
            else:
                async with bot.conversation(event.chat_id) as conv:
                    await conv.send_message('Send hits you want to add.')
                    try:
                        response = await conv.get_response()
                    except:
                        return
                    if response.text[0] == "/":
                        return
            hits = response.raw_text.split("\n")
            count = 0
            for hit in hits:
                hit=hit.strip()
                hit = hit.split(" ")[0]
                if ":" in hit:
                    if hit[0] == "[":
                        mail, pwd = hit.split("):", maxsplit = 1)
                        hit = mail[mail.index("[") + 1 : mail.index("]")] + ":" + pwd
                    hit = hit.split("|")[0].split(" ")[0]
                    if not hitExists(hit):
                        addHit(hit)
                        count += 1
            await bot.send_message(event.chat_id, f"{count} Hit(s) added.")
        if '/deletehits' == event.raw_text.lower():
            async with bot.conversation(event.chat_id) as conv:
                await conv.send_message('Send hits you want to remove.')
                try:
                    response = await conv.get_response()
                except:
                    return
                if response.text[0] == "/":
                    return
                hits = response.raw_text.split("\n")
                count = 0
                for hit in hits:
                    hit = hit.strip()
                    hit = hit.split(" ")[0]
                    if ":" in hit:
                        if hit[0] == "[":
                            mail, pwd = hit.split("):", maxsplit = 1)
                            hit = mail[mail.index("[") + 1 : mail.index("]")] + ":" + pwd
                        hitID = hitExists(hit).hitID
                        if hitID:
                            remHit(hitID)
                            count += 1
                await conv.send_message(f"{count} Hit(s) removed.")
        if '/cleanhits' == event.raw_text.lower():
            hitList = get_all_hits()
            for hit in hitList:
                try:
                    remHit(hit.hitID)
                except:
                    pass
            await bot.send_message(event.chat_id, "Cleaned...")
        if '/reset' == event.raw_text.lower():
            resetMsg = await bot.send_message(event.chat_id, "Resetting...")
            await reset(resetMsg) 
        if '/search' == event.raw_text.lower()[0:7]:
            try:
                ID = int(event.raw_text.lower()[7:])
            except:
                await bot.send_message(event.chat_id, "Error")
                return
            try:
                entity = await bot.get_entity(ID)
            except:
                await bot.send_message(event.chat_id, "Not found")
                return
            user = get_user(ID)
            msg = f"ID = {ID}\n"
            msg += f"First name = {entity.first_name}\n"
            msg += f"Last name = {entity.last_name}\n"
            if entity.username:
                msg += f"Username = @{entity.username}\n"
            else:
                msg += "Username = None\n"
            if user:
                msg += f"Daily Limit = {user.dailylimit}/{Var.dailyLimit}"
            await bot.send_message(event.chat_id, msg)
        elif event.raw_text == "/broadcast":
            try:
                previous_message = await event.get_reply_message()
                if previous_message.media:
                    await bot.send_message(event.chat_id, "Reply to a text msg")
                    time.sleep(1)
                    await event.delete()
                    return
                try:
                    msg = previous_message.text
                except:
                    await bot.send_message(event.chat_id, event.message.id, "Reply to a text msg")
                    time.sleep(1)
                    await event.delete()
                    return
                userList = get_all_users()
                if len(userList) == 0:
                    msg = "No user found"
                else:
                    bMsg = await bot.send_message(event.chat_id, f"Sending to {len(userList)} users.")
                    err = 0 
                    succ = 0
                    count = 0
                    errs = ""
                    for user in userList:
                        try:
                            await bot.send_message(int(user.userId), msg)
                            succ += 1
                        except Exception as e:
                            err += 1
                            errs += f"Userid - {user.userId} Error - {e}\n"
                        count += 1
                        percents = round(100.0 * count / float(len(userList)), 1)
                        try:
                            await bot.edit_message(event.chat_id, bMsg.id, f"Sending... [{percents}%]\n{err} error(s) till now.")
                        except:
                            pass
                    await bot.edit_message(event.chat_id, bMsg.id, f"Successfully sent to {succ} users with {err} errors.")
            except Exception as error:
                await bot.send_message(event.chat_id, "Reply to a text msg")
    if 'yo' == event.raw_text.lower():
        await event.reply('yo')
        return

async def reset(resetMsg = None):
    msg = "Limit Has Been Reset , You can Generate Your Accounts Now !"
    users = exceededLimitUsers(Var.dailyLimit)
    count = 0
    for user in users:
        try:
            await bot.send_message(int(user.userId), msg)
        except Exception as e:
            pass
        count += 1
        if resetMsg:
            percents = round(100.0 * count / float(len(users)), 1)
            try:
                await bot.edit_message(resetMsg.chat_id, resetMsg.id, f"Sending... [{percents}%]")
            except:
                pass
    resetDailyLimit()
    if resetMsg:
        await bot.edit_message(resetMsg.chat_id, resetMsg.id, "Done")   
    



@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"report_(.*)")))
async def genAcc(event):
    hitID = event.data_match.group(1).decode("UTF-8")
    try:
        hit = get_hit_by_id(hitID)
        email, pwd = hit.hit.split(":", maxsplit = 1)
        entity = await bot.get_entity(event.chat_id)
        username = entity.username
        user = get_user(event.chat_id)
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
            username = username,
            dailyLimit = user.dailylimit,
            TotalDailyLimit = Var.dailyLimit
        )
        button = [
            [(Button.inline("Remove Now", data=f"remove_{hitID}"))],
            [(Button.inline("Ignore", data="ignore"))]
        ]
        if Var.repotGroupId:
            await bot.send_message(Var.repotGroupId, msg, buttons=button)
        else:
            await bot.send_message(Var.ownerIDs[0], msg, buttons=button)
    except:
        pass
    await event.answer("Report Sent to Admins!", alert=True)
    newButton = [Button.url("Authentication error?", "https://bit.ly/35gd38D")]
    await bot.edit_message(event.chat_id, event.query.msg_id, buttons = newButton)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"remove_(.*)")))
async def genAcc(event):
    if event.query.user_id not in Var.ownerIDs:
        await event.answer("Access Denied")
        return
    hitID = event.data_match.group(1).decode("UTF-8")
    try:
        if get_hit_by_id(hitID):
            remHit(hitID)
            await event.answer("Removed.", alert=True)
            await event.delete()
        else:
            await event.answer("Hits already removed.", alert=True)
            await event.delete()
    except Exception as e:
        if Var.repotGroupId:
            await bot.send_message(Var.repotGroupId, f"Error - {e}")
        else:
            await bot.send_message(Var.ownerIDs[0], f"Error - {e}")


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ignore")))
async def genAcc(event):
    if event.query.user_id not in Var.ownerIDs:
        await event.answer("Access Denied")
        return
    await event.delete()



scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(reset, 'cron', hour=0)
scheduler.start()



print("Bot Started.")
bot.run_until_disconnected()