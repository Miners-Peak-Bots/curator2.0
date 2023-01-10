from user.models import (
    TeleUser
)
from bot.utils.msg import (
    sched_cleanup
)
from group.models import Group
from bot.utils.user import (
    get_target_user,
    get_reason
)
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPermissions
from ...utils.msg import errorify
from bot.utils.msg import log
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_unmute(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        reply = msg.reply_text('Admin not found')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    try:
        user = get_target_user(msg)
    except Exception as e:
        reply = msg.reply_text(str(e))
        sched_cleanup(reply)
        return False

    try:
        reason = get_reason(msg)
    except Exception:
        reply = msg.reply_text('Please specify a reason to unmute')
        sched_cleanup(reply)
        return False

    if user.is_admin:
        msg.delete()
        return False

    client.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=user.tele_id,
        permissions=ChatPermissions()
    )
    user.log(message=reason, event=5)

    response = (
        f'🎤 {msg.from_user.mention} unmuted {user.mention}'
    )
    log_msg = f'{response}\nChat: {msg.chat.title}'
    log(client, log_msg)
    msg.delete()
    reply = client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )
    sched_cleanup(reply)


def handle_unmuteall(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        reply = msg.reply_text('Admin not found')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    try:
        user = get_target_user(msg)
    except Exception as e:
        reply = msg.reply_text(str(e))
        sched_cleanup(reply)
        return False

    try:
        reason = get_reason(msg)
    except Exception:
        reply = msg.reply_text('Please specify a reason to warn')
        sched_cleanup(reply)
        return False

    if user.is_admin:
        msg.delete()
        return False

    errors = []
    for group in Group.objects.all():
        try:
            client.restrict_chat_member(
                chat_id=group.group_id,
                user_id=user.tele_id,
                permissions=group.get_permissions()
            )
        except Exception as e:
            errors.append(
                f'Could not unmute {user.tele_id} '
                f'on chat {group.title}({group.group_id}) due to '
                f'{str(e)}')

    user.log(message=reason, event=5)
    response = (
        f'🎤 {msg.from_user.mention} globally unmuted {user.mention}'
    )
    log_msg = errorify(response, errors)
    log(client, log_msg)
    msg.delete()
    reply = client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )
    sched_cleanup(reply)


__HANDLERS__ = [
    MessageHandler(handle_unmute,
                   filters.command('unmute', prefixes=CMD_PREFIX)),
    MessageHandler(handle_unmuteall, filters.command(
        'unmuteall', prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    '$unmute: Unmute a user in the current group\n'
    '    $unmute 567319\n'
    '    $unmute @username\n'
    '    Reply to a user\'s message with $unmute'
    '$unmuteall: Unmute a user from all the groups\n'
    '    $unmute 567319\n'
    '    $unmute @username\n'
    '    Reply to a user\'s message with $unmute'
)
