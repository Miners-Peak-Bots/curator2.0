from pyrogram.handlers import MessageHandler
from django.conf import settings
from pyrogram import filters


__HELP__ = 'Help text'


async def handle_purge(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        await msg.delete()
        return False

    if not msg.reply_to_message:
        await msg.delete()
        return False

    target_msg = msg.reply_to_message
    purge_list = list(range(target_msg.id, msg.id+1))

    reason = None
    if len(msg.command) > 1:
        reason = ' '.join(msg.command[1:])
    print(reason)
    try:
        await client.delete_messages(msg.chat.id,
                                     purge_list,
                                     revoke=True)
    except Exception:
        try:
            await msg.delete()
        except Exception:
            pass
        await client.send_message(msg.chat.id, 'Failed. Purge manually please')
        return False


__HANDLERS__ = [
    MessageHandler(handle_purge, filters.command('purge', prefixes='!')),
]
