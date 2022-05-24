from group.models import Group
from user.utils import create_get_user
from ...utils.msg import errorify
from django.conf import settings
from pyrogram.types import ChatPrivileges
from pyrogram.handlers import MessageHandler
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


def handle_promote(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    member = msg.reply_to_message.from_user
    member, created = create_get_user(member)
    member.admin = True
    member.save()

    errors = []
    for group in Group.objects.all():
        client.resolve_peer(group.group_id)
        privileges = group.get_admin_privileges()
        try:
            client.promote_chat_member(chat_id=group.group_id,
                                       user_id=member.tele_id,
                                       privileges=privileges)
        except Exception as e:
            errors.append(
                f'Could not promote user in {group.group_id} due to '
                f'{str(e)}. Please promote manually or retry'
            )

    response = errorify('User has been promoted', errors)
    msg.reply_text(response)


def handle_demote(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    member = msg.reply_to_message.from_user
    member, created = create_get_user(member)
    member.admin = False
    member.save()
    errors = []
    privileges = ChatPrivileges(can_manage_chat=False)
    for group in Group.objects.all():
        client.resolve_peer(group.group_id)
        try:
            client.promote_chat_member(chat_id=group.group_id,
                                       user_id=member.tele_id,
                                       privileges=privileges)
        except Exception as e:
            errors.append(
                f'Could not remove as admin in {group.group_id} due to\n'
                f'{str(e)}. Please demote manually or retry'
            )

    response = errorify('User has been demoted', errors)
    msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_promote, filters.command('promote', prefixes='!')),
    MessageHandler(handle_demote, filters.command('demote', prefixes='!')),
]
