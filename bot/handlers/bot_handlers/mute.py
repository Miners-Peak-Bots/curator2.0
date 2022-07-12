from user.models import (
    TeleUser
)
from group.models import Group
from bot.utils.user import get_target_user_and_reason
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPermissions
from ...utils.msg import errorify


def handle_mute(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    try:
        data = get_target_user_and_reason(msg, ommit='!mute')
    except Exception as e:
        return msg.reply_text(str(e))

    user = data['user']
    reason = data['reason']

    if user.is_admin:
        msg.delete()
        return False

    client.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=data['user'].tele_id,
        permissions=ChatPermissions()
    )

    response = (
        f'🔇 {msg.from_user.mention} muted {user.mention} for\n'
        f'<b>Reason:</b> {reason.strip()}\n'
        # f'Warn {warns}/3'
    )
    msg.delete()
    client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )


def handle_muteall(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    try:
        data = get_target_user_and_reason(msg, ommit='!muteall')
    except Exception as e:
        return msg.reply_text(str(e))

    user = data['user']
    reason = data['reason']

    if user.is_admin:
        msg.delete()
        return False

    errors = []
    for group in Group.objects.all():
        try:
            client.restrict_chat_member(
                chat_id=group.group_id,
                user_id=data['user'].tele_id,
                permissions=ChatPermissions()
            )
        except Exception as e:
            errors.append(
                f'Could not mute {user.tele_id} '
                f'on chat {group.group_id} due to '
                f'{str(e)}')

    response = (
        f'🔇 {msg.from_user.mention} globally muted {user.mention} for\n'
        f'<b>Reason:</b> {reason.strip()}\n'
        # f'Warn {warns}/3'
    )
    response = errorify(response, errors)
    msg.delete()
    client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )


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
