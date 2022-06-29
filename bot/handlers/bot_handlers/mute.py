from user.models import (
    TeleUser
)
from bot.utils.user import get_target_user_and_reason
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPermissions


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
        data = get_target_user_and_reason(msg)
    except Exception:
        return msg.reply_text('User not found')

    client.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=data['user'].tele_id,
        permissions=ChatPermissions()
    )


__HANDLERS__ = [
    MessageHandler(handle_mute, filters.command('warn', prefixes='!')),
]

__HELP__ = ''
