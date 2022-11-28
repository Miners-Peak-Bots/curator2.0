from pyrogram.handlers import MessageHandler
from pyrogram import filters
from django.conf import settings
from group.utils import create_get_group
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_logging(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    try:
        log_id = msg.command[1]
    except IndexError:
        msg.reply_text('Please mention a destination group id')
        return False

    try:
        log_id = int(log_id)
    except ValueError:
        msg.reply_text('Please use a valid group id')

    group, created = create_get_group(msg.chat)
    group.log_channel = log_id
    group.save()
    msg.reply_text('Group log has been set.')


def handle_logging_off(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    group, created = create_get_group(msg.chat)
    group.log_channel = None
    group.save()
    msg.reply_text('Logging disabled')


def handle_group_id(client, msg):
    msg.reply_text(msg.chat.id)


__HANDLERS__ = [
    MessageHandler(handle_logging,
                   (filters.command('logging',
                                    prefixes=CMD_PREFIX) & filters.group)),
    MessageHandler(handle_group_id,
                   (filters.command('groupid',
                                    prefixes=CMD_PREFIX) & filters.group)),
    MessageHandler(handle_logging_off,
                   (filters.command('log_off',
                                    prefixes=CMD_PREFIX) & filters.group))
]


__HELP__ADMIN__ = (
    '$logging: Enable logging for a group\n'
    '    $logging {group_id}\n'
    '    Example: !logging -10054341412\n'
    '$log_off: Disable logging for a group\n'
    '     Send $log_off in the group to disable logging'
)
