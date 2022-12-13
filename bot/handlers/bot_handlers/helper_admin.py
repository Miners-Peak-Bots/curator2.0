from group.models import Group
from ...utils.msg import errorify
from django.conf import settings
from pyrogram.types import ChatPrivileges
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from bot.utils.user import get_target_user
from bot.utils.msg import log
from bot.utils.msg import sched_cleanup

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_add_helper(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    try:
        member = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)
        return False

    member.admin = True
    member.helper_admin = True
    member.save()

    errors = []
    for group in Group.objects.all():
        client.resolve_peer(group.group_id)
        privileges = group.get_admin_privileges()
        try:
            client.promote_chat_member(chat_id=group.group_id, user_id=member.tele_id, privileges=privileges)
        except Exception as e:
            errors.append(
                f'Could not promote user in {group.group_id} due to ' f'{str(e)}. Please promote manually or retry'
            )

    log_msg = errorify(f'{member.mention} can verify members', errors)
    log(client, log_msg)
    reply = msg.reply_text(f'{member.mention} can verify members')
    sched_cleanup(reply)
    sched_cleanup(msg)


def handle_remove_helper(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    try:
        member = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)
        return False

    member.admin = False
    member.helper_admin = False
    member.save()
    errors = []
    privileges = ChatPrivileges(can_manage_chat=False)
    for group in Group.objects.all():
        client.resolve_peer(group.group_id)
        try:
            client.promote_chat_member(chat_id=group.group_id, user_id=member.tele_id, privileges=privileges)
        except Exception as e:
            errors.append(
                f'Could not remove as admin in {group.group_id} due to\n' f'{str(e)}. Please demote manually or retry'
            )

    log_msg = errorify(f'{member.mention} cannot verify members', errors)
    log(client, log_msg)
    reply = msg.reply_text(f'{member.mention} cannot verify members')
    sched_cleanup(reply)
    sched_cleanup(msg)


__HANDLERS__ = [
    MessageHandler(handle_add_helper, filters.command('add_helper_admin', prefixes=CMD_PREFIX)),
    MessageHandler(handle_remove_helper, filters.command('remove_helper_admin', prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    '$add_helper_admin: Promote a user to admin and can verify members\n'
    '    $add_helper_admin 567319\n'
    '    $add_helper_admin @username Flooding chat\n'
    '    Reply to a user\'s message with $add_helper_admin\n'
    '$remove_helper_admin:- Remove a user as admin\n'
    '    $remove_helper_admin 567319\n'
    '    $remove_helper_admin @username\n'
    '    Reply to a user\'s message with $remove_helper_admin'
)
