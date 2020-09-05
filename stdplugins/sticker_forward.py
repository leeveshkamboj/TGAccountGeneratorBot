from telethon import events, Button
from uniborg.util import admin_cmd
import time

channel_id = -1001481026778
msg_id = 211
sticker_delete = False
footer = "\n\n➖🔰@PandaZnetwork🔰➖"
img = {-1001481026778 : "https://i.imgur.com/fQi4wJe.jpg"}



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
                await event.client.send_message(
                    event.chat_id,
                    event.text + footer,
                    file = img[event.chat_id],
                    link_preview = False
                )
                await event.delete()
            except:
                pass
            await borg.forward_messages(channel_id, msg_id, channel_id)


