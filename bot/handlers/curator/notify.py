from ...utils.msg import errorify
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from group.models import Group
from bot.utils.msg import (
    sched_cleanup
)
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_notify(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
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
    reply = msg.reply_text(response)
    sched_cleanup(reply)
    sched_cleanup(msg)


__HANDLERS__ = [
    MessageHandler(handle_notify,
                   (filters.command('notification', prefixes=CMD_PREFIX) &
                    filters.private))
]


__HELP__ADMIN__ = (
    '$notification: Send a network side message(admin only)\n'
    '   Reply to a message with !notification'
)
