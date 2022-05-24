from ...utils.msg import errorify
from pyrogram.handlers import MessageHandler
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


async def handle_notify(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        await msg.delete()
        return False

    message = msg.text.replace('!notification', '').strip()
    if not len(message) > 0:
        await msg.reply_text('Please provide a valid message')

    errors = []
    for group in Group.select():
        try:
            await client.send_message(group.group_id, message)
        except Exception as e:
            errors.append(
                f'Failed to notify {group.group_id} due to {str(e)}'
            )

    response = errorify('Done!', errors)
    await msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_notify,
                   (filters.command('notification', prefixes='!') &
                    filters.private))
]
