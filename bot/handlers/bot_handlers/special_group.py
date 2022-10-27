from group.utils import create_get_group
from django.conf import settings
from pyrogram import filters
from pyrogram.handlers import MessageHandler
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_makespecial(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    group, created = create_get_group(msg.chat)
    group.vendor = True
    group.save()
    return msg.reply_text(
        'Group has been marked as special.\n'
        'Please set privileges and flair from dashboard'
    )


def handle_removespecial(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    group, created = create_get_group(msg.chat)
    if created:
        msg.delete()
        return msg.reply_text('Group is not special currently')

    group.vendor = False
    group.save()
    return msg.reply_text('Group has been removed from special groups.')


__HANDLERS__ = [
    MessageHandler(handle_makespecial,
                   (filters.command('vendor', prefixes=CMD_PREFIX) &
                    filters.group)),
    MessageHandler(handle_removespecial,
                   (filters.command('novendor', prefixes=CMD_PREFIX) &
                    filters.group)),
]


__HELP__ADMIN__ = (
    '$vendor: Set vendor status to group\n'
    '$novendor: Remove vendor status from group'
)
