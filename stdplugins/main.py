from telethon import events, Button
from uniborg.util import admin_cmd
import time

channel_id = -1001481026778
msg_id = 211
sticker_delete = False
footer = "\n\n**__➖🔰@PandaZnetwork🔰➖__**"
img = {-1001481026778 : "https://i.imgur.com/fQi4wJe.jpg", -1001481899343 : "https://i.imgur.com/DRUnSIc.jpg", -1001122798596 : "https://i.imgur.com/mGgAIbl.jpg", -1001251394025 : "https://i.imgur.com/NG6M6Eh.jpg", -1001351480003 : "https://i.imgur.com/rhXRIKw.jpg"}
name = {-1001481026778 : "Express VPN", -1001481899343 : "Windscribe", -1001122798596 : "IP Vanish", -1001251394025 : "Hulu", -1001351480003 : "DisneyPlus"}


@borg.on(events.NewMessage)
async def my_event_handler(event):                     
    global channel_id, msg_id, sticker_delete, footer, img
    if channel_id is not None and msg_id is not None and event.chat_id in img.keys():
        if event.sticker is not None:
            if sticker_delete:
                await event.delete()
        elif event.gif is not None or event.poll is not None:
            return
        else:
            try:
                if event.chat_id in name.keys() and ("http://" in event.text or "https://" in event.text):
                    msg = f'''**__🔰{name[event.chat_id]}[Valid Hits]🔰

🌀 All accounts are working and fresh. We will never give Not working Accounts

✅ If these accounts have guard then sorry we can't help. 
==========================
⭕️ Link to Accounts :
🔥 {event.text}
==========================
❌ Don't change the password else account will stop soon
➖➖➖➖➖➖➖➖➖➖➖➖
ENJOY ❤️👍

➖🔰@PandaZnetwork🔰➖__**'''
                else:
                    msg = f"**__🔰{name[event.chat_id]}🔰__**\n\n" + event.text + footer
                await event.client.send_message(
                    event.chat_id,
                    msg,
                    file = img[event.chat_id],
                    link_preview = False
                )
                await event.delete()
            except:
                pass
            await borg.forward_messages(event.chat_id, msg_id, channel_id)


