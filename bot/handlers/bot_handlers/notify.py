from ...utils.msg import errorify
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from group.models import Group
from django.conf import settings


__HELP__ = """Hey man
How is it going"""


def handle_notify(client, msg):
    print('i am running')
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    message = msg.reply_to_message.text
    errors = []
    for group in Group.objects.all():
        try:
            client.send_message(group.group_id, message)
        except Exception as e:
            errors.append(
                f'Failed to notify {group.group_id} due to {str(e)}'
            )

    response = errorify('Done!', errors)
    msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_notify,
                   (filters.command('notification', prefixes='!') &
                    filters.private))
]
