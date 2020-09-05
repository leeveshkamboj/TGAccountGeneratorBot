from telethon import events

@borg.on(events.NewMessage)
async def my_event_handler(event):
    if not event.is_channel and '/start' in event.raw_text.lower():
        await borg.send_message(event.chat_id, "For @PandaZnetwork.\n\n**Made by @HeisenbergTheDanger**")
    elif not event.is_channel and 'yo' in event.raw_text.lower():
        await event.reply('yo')
