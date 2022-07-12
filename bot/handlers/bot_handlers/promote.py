from group.models import Group
from ...utils.msg import errorify
from django.conf import settings
from pyrogram.types import ChatPrivileges
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from bot.utils.user import get_target_user


def handle_promote(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    try:
        member = get_target_user(msg)
    except Exception:
        return msg.reply_text('User not found')

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

    try:
        member = get_target_user(msg)
    except Exception:
        return msg.reply_text('User not found')

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


__HELP__ = (
    '!promote: Promote a user to admin\n'
    '    !promote 567319\n'
    '    !promote @username Flooding chat\n'
    '    Reply to a user\'s message with !promote\n'
    '!demote:- Remove a user as admin\n'
    '    !demote 567319\n'
    '    !demote @username\n'
    '    Reply to a user\'s message with !demote'
)
