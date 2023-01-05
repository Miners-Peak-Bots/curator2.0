from pyrogram.handlers import MessageHandler
from django.conf import settings
from pyrogram import filters
# from django.core.cache import cache
from ...utils.msg import sched_cleanup
from group.models import Group
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_toggle(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    try:
        group = Group.objects.get(pk=msg.chat.id)
    except Group.DoesNotExist:
        msg.delete()
        return False

    group.antispam = not group.antispam
    group.save()
    sent = msg.reply_text(
        f'Antispam has been set to {group.antispam}'
    )
    sched_cleanup(msg)
    sched_cleanup(sent)


__HANDLERS__ = [
    MessageHandler(handle_toggle, filters.command('antispam',
                                                  prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    '$antispam: Toggle antispam for the group\n'
)
