from telethon import events

@borg.on(events.NewMessage)
async def my_event_handler(event):
    if not event.is_channel:
        if '/start' == event.raw_text.lower():
            await borg.send_message(event.chat_id, "**Made by @HeisenbergTheDanger for @PandaZnetwork.**")
            return
        if 'yo' == event.raw_text.lower():
            await event.reply('yo')
            return
        out = event.raw_text.split("|")
        with io.BytesIO(str.encode(out[1].lstrip())) as out_file:
            out_file.name = out[0].rstrip() + ".txt"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
            )
