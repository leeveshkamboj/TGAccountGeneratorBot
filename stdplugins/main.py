from telethon import events, Button
from uniborg.util import admin_cmd
import time


channel_id = -1001481026778
msg_id = 211
sticker_delete = False
footer = "\n\n**__➖🔰@PandaZnetwork🔰➖__**"
img = {-1001481026778 : "https://i.imgur.com/fQi4wJe.jpg", -1001481899343 : "https://i.imgur.com/DRUnSIc.jpg", -1001122798596 : "https://i.imgur.com/mGgAIbl.jpg", -1001251394025 : "https://i.imgur.com/NG6M6Eh.jpg", -1001351480003 : "https://i.imgur.com/rhXRIKw.jpg", -1001313593468 : "https://i.imgur.com/tL2awKR.jpg"}
name = {-1001481026778 : "Express VPN", -1001481899343 : "Windscribe", -1001122798596 : "IP Vanish", -1001251394025 : "Hulu", -1001351480003 : "DisneyPlus",  -1001313593468: "Nord VPN"}
paused = False

multiChannelId = {-1001177011841 : "Antivirus"}
multiName = {"Antivirus" : ["mc", "avast", "bd"]}
multiImg = {"mc" : "https://i.imgur.com/EhwhNyI.jpg", "avast" : "https://i.imgur.com/5S4zREv.jpg", "bd" : "https://i.imgur.com/iBlJ3lf.jpg"}
multiFullName = {"mc" : "McAfee", "avast": "Avast", "bd": "Bit Defender"}


def generateMsg(name, content):
    if "http://" in content.lower() or "https://" in content.lower():
        return f'''**__🔰{name}[Valid Hits]🔰

🌀 All accounts are working and fresh. We will never give Not working Accounts

✅ If these accounts have guard then sorry we can't help. 

🔺 How to Open Links
Link:- https://youtu.be/XkMSDlGEKqQ
==========================
⭕️ Link to Accounts :
🔥 {content}
==========================
❌ Don't change the password else account will stop soon
➖➖➖➖➖➖➖➖➖➖➖➖
ENJOY ❤️👍

➖🔰@PandaZnetwork🔰➖__**'''
    else:
        return f"**__🔰{name}🔰__**\n\n" + content + footer




@borg.on(events.NewMessage)
async def my_event_handler(event):                     
    global channel_id, msg_id, sticker_delete, footer, img, paused, name, multiChannelId, multiName, multiImg, multiFullName
    if event.text == "/stop":
        paused = True
        await event.edit("Bot Stopped.")
        time.sleep(3)
        await event.delete()
        return
    if event.text == "/start":
        paused = False
        await event.edit("Bot Started.")
        time.sleep(3)
        await event.delete()
        return
    if paused:
        return
    if event.sticker:
        if sticker_delete:
            await event.delete()
    elif not event.web_preview and (event.gif or event.poll or event.media):
        try:
            await borg.edit_message(event.chat_id, event.message.id, event.text + footer, link_preview = False)
        except:
            pass
        if channel_id and msg_id:
            await borg.forward_messages(event.chat_id, msg_id, channel_id)
        return
    else:
        try:
            if event.chat_id in img.keys():
                msg = generateMsg(name[event.chat_id], event.text)
                image = img[event.chat_id]
            elif event.chat_id in multiChannelId.keys():
                for name in multiName[multiChannelId[event.chat_id]]:
                    if name in event.text.lower() and "|" in event.text:
                        image = multiImg[name]
                        msg = generateMsg(multiFullName[name], event.text[event.text.index("|") + 1 :].strip())
                        break
                else:
                    await borg.edit_message(event.chat_id, event.message.id, event.text + footer, link_preview = False)
                    if channel_id and msg_id:
                        await borg.forward_messages(event.chat_id, msg_id, channel_id)
                    return
            else:
                return
            await event.client.send_message(
                event.chat_id,
                msg,
                file = image,
                link_preview = False
            )
            await event.delete()
        except Exception as err:
            print(f"Error - {err}")
        if channel_id and msg_id:
            await borg.forward_messages(event.chat_id, msg_id, channel_id)


