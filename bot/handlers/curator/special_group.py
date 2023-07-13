import time

from django.conf import settings
from group.utils import create_get_group
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from user.models import TeleUser

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_makespecial(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    group, created = create_get_group(msg.chat)
    group.vendor = True
    group.save()
    for user in TeleUser.objects.filter(verified=True):
        privileges = group.get_special_privileges()
        try:
            client.promote_chat_member(chat_id=group.group_id, user_id=user.tele_id, privileges=privileges)
            time.sleep(2)
            if group.flair:
                print("Setting flair to ", group.flair)
                client.set_administrator_title(group.group_id, user.tele_id, group.flair)
        except Exception:
            pass

    return msg.reply_text('Group has been marked as special.\n' 'Please set privileges and flair from dashboard')


def handle_removespecial(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
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
    MessageHandler(handle_makespecial, (filters.command('vendor', prefixes=CMD_PREFIX) & filters.group)),
    MessageHandler(handle_removespecial, (filters.command('novendor', prefixes=CMD_PREFIX) & filters.group)),
]


__HELP__ADMIN__ = '$vendor: Set vendor status to group\n' '$novendor: Remove vendor status from group'
