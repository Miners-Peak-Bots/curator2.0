from user.models import (
    TeleUser
)
from group.models import Group
from bot.utils.user import (
    get_target_user,
    get_reason
)
from bot.utils.msg import (
    sched_cleanup
)
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPermissions
from ...utils.msg import errorify
from bot.utils.msg import log


def handle_mute(client, msg):
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
    except Exception:
        reply = msg.reply_text('User could not be found')
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

    client.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=user.tele_id,
        permissions=ChatPermissions()
    )
    user.log(message=reason, event=4)
    response = (
        f'🔇 {msg.from_user.mention} muted {user.mention} for\n'
        f'<b>Reason:</b> {reason.strip()}\n'
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


def handle_muteall(client, msg):
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
    except Exception:
        reply = msg.reply_text('User could not be found')
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
                permissions=ChatPermissions()
            )
        except Exception as e:
            errors.append(
                f'Could not mute {user.tele_id} '
                f'on chat {group.group_id} due to '
                f'{str(e)}')

    user.log(message=reason, event=4)
    response = (
        f'🔇 {msg.from_user.mention} globally muted {user.mention} for\n'
        f'<b>Reason:</b> {reason.strip()}\n'
        # f'Warn {warns}/3'
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
    MessageHandler(handle_mute, filters.command('mute', prefixes='!')),
    MessageHandler(handle_muteall, filters.command('muteall', prefixes='!')),
]

__HELP__ = (
    '!mute: mute a user in the current group\n'
    '    !mute 567319\n'
    '    !mute @username\n'
    '    Reply to a user\'s message with !mute'
    '!muteall: mute a user from all the groups\n'
    '    !mute 567319\n'
    '    !mute @username\n'
    '    Reply to a user\'s message with !mute'
)
