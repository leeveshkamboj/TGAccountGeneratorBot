from telethon import events
import io


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
        filename = out[0].rstrip() + ".txt"
        
        if len(out) < 2:
            filename = "unnamed.txt"
            text = event.raw_text
        else:
            text = ''
            for a in out[1:]:
                text += a + "|"
        with io.BytesIO(str.encode(text)) as out_file:
            out_file.name = filename
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
            )
