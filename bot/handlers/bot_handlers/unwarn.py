from user.models import (
    TeleUser
)
from bot.utils.user import get_target_user
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode


def handle_unwarn(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    try:
        victim = get_target_user(msg)
    except Exception:
        return msg.reply_text('User not found')

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    if not victim.warning.count():
        msg.delete()
        return False

    warning = victim.warning.last()
    warning.delete()

    response = (
        f'❎ {msg.from_user.mention} unwarned {victim.mention} for\n'
        f'<b>Reason:</b> {warning.reason.strip()}'
    )
    client.send_message(msg.chat.id, response, parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(handle_unwarn, filters.command('unwarn', prefixes='!')),
]

__HELP__ = (
    "!unwarn: Remove a user's latest warn"
    '    !unwarn 567319\n'
    '    !unwarn @username\n'
    '    Reply to a user\'s message with !unwarn'
)
