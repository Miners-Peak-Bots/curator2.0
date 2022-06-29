from user.models import (
    TeleUser
)
from group.models import Group
from bot.utils.user import get_target_user
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPermissions
from ...utils.msg import errorify


def handle_unmute(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    try:
        user = get_target_user(msg)
    except Exception as e:
        return msg.reply_text(str(e))

    if user.is_admin:
        msg.delete()
        return False

    client.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=user.tele_id,
        permissions=ChatPermissions()
    )

    response = (
        f'🎤 {msg.from_user.mention} unmuted {user.mention}'
    )
    msg.delete()
    client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )


def handle_unmuteall(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    try:
        user = get_target_user(msg)
    except Exception as e:
        return msg.reply_text(str(e))

    if user.is_admin:
        msg.delete()
        return False

    errors = []
    for group in Group.objects.all():
        try:
            client.restrict_chat_member(
                chat_id=msg.chat.id,
                user_id=user.tele_id,
                permissions=ChatPermissions()
            )
        except Exception as e:
            errors.append(
                f'Could not mute {user.tele_id} '
                f'on chat {group.group_id} due to '
                f'{str(e)}')

    response = (
        f'🎤 {msg.from_user.mention} globally unmuted {user.mention}'
    )
    response = errorify(response, errors)
    msg.delete()
    client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )


__HANDLERS__ = [
    MessageHandler(handle_unmute, filters.command('unmute', prefixes='!')),
    MessageHandler(handle_unmuteall, filters.command(
        'unmuteall', prefixes='!')),
]

__HELP__ = ''
