from group.utils import create_get_group
from django.conf import settings
from pyrogram import filters
from pyrogram.handlers import MessageHandler

__HELP__ = ''


def handle_makespecial(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    group, created = create_get_group(msg.chat)
    group.special = True
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

    group.speical = False
    group.save()
    return msg.reply_text('Group has been removed from special groups.')


__HANDLERS__ = [
    MessageHandler(handle_makespecial,
                   (filters.command('special', prefixes='!') &
                    filters.group)),
    MessageHandler(handle_removespecial,
                   (filters.command('notspecial', prefixes='!') &
                    filters.group)),
]
